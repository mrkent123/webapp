#!/usr/bin/env python3
"""
WebSocket Reload Server
Listens for file changes and sends reload messages to connected clients.
Also provides an HTTP endpoint for remote devices (like iPhone via AirPlay).
"""

import asyncio
import websockets
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import urllib.parse


# Global variable to store connected WebSocket clients
connected_clients = set()


class ReloadServer:
    def __init__(self, ws_port=3210, http_port=3211):
        self.ws_port = ws_port
        self.http_port = http_port
        self.clients = set()
        
    async def register_client(self, websocket):
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        
    async def unregister_client(self, websocket):
        self.clients.discard(websocket)
        print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def handler(self, websocket, path):
        await self.register_client(websocket)
        try:
            async for message in websocket:
                # Echo message back (for testing)
                print(f"Received message: {message}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def broadcast_reload(self):
        if not self.clients:
            print("No clients connected to broadcast reload to")
            return
            
        print(f"Broadcasting reload to {len(self.clients)} clients")
        # Create a task for each client to send the reload message
        tasks = [client.send("reload") for client in self.clients.copy() 
                 if not client.closed]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def start_websocket_server(self):
        print(f"Starting WebSocket server on ws://localhost:{self.ws_port}")
        start_server = websockets.serve(self.handler, "localhost", self.ws_port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/reload':
            # Trigger reload
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Reload triggered')
            
            # Call the reload function in the main thread
            import threading
            threading.Thread(target=self.server.reload_callback, args=(), daemon=True).start()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
    
    def log_message(self, format, *args):
        # Suppress standard HTTP request logging
        pass


class HTTPServerThread(threading.Thread):
    def __init__(self, port, reload_callback):
        threading.Thread.__init__(self)
        self.port = port
        self.reload_callback = reload_callback
        self.httpd = None
        
    def run(self):
        print(f"Starting HTTP server on http://localhost:{self.port}")
        
        # Create HTTP request handler class with reload callback
        class CustomHTTPRequestHandler(HTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.server.reload_callback = reload_callback
                super().__init__(*args, **kwargs)
        
        # Update handler class
        HTTPRequestHandler.reload_callback = self.reload_callback
        
        # Start the server
        self.httpd = HTTPServer(('localhost', self.port), CustomHTTPRequestHandler)
        self.httpd.serve_forever()
    
    def stop(self):
        if self.httpd:
            self.httpd.shutdown()


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    # Create reload server instance
    reload_server = ReloadServer(ws_port=3210, http_port=3211)
    
    # Define the reload callback function
    def reload_callback():
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Broadcast reload to all WebSocket clients
        loop.run_until_complete(reload_server.broadcast_reload())
        loop.close()
    
    # Start HTTP server in a separate thread
    http_server_thread = HTTPServerThread(3211, reload_callback)
    http_server_thread.daemon = True
    http_server_thread.start()
    
    # Print server info
    local_ip = get_local_ip()
    print(f"WebSocket server listening on: ws://localhost:{reload_server.ws_port}")
    print(f"HTTP reload server listening on: http://{local_ip}:{reload_server.http_port}/reload")
    print(f"Use this URL on your iPhone to trigger reload: http://{local_ip}:{reload_server.http_port}/reload")
    
    # Start WebSocket server in the main thread
    reload_server.start_websocket_server()


if __name__ == "__main__":
    main()