#!/usr/bin/env python3
"""
Simple Reload Server with HTTP Endpoint
Provides an HTTP endpoint to trigger reloads for connected clients.
"""

import threading
import json
import time
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket


class ReloadServer:
    def __init__(self, port=35729):
        self.port = port
        self.clients = set()  # Track connected clients (for future WebSocket support)
        
    def start(self):
        # Create HTTP request handler class with reload server instance
        class ReloadHTTPRequestHandler(BaseHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.reload_server = reload_server_instance
                super().__init__(*args, **kwargs)

            def do_GET(self):
                if self.path == '/reload':
                    # Trigger full reload
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Reload triggered')
                    
                    print("Full reload triggered via HTTP GET")
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not found')

            def do_POST(self):
                if self.path == '/reload':
                    # Read the content length and body
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode('utf-8')
                    
                    try:
                        # Parse the JSON payload
                        payload = json.loads(post_data)
                        reload_type = payload.get('type', 'FULL_RELOAD')
                        
                        # Send appropriate response
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        
                        response_data = {
                            "status": "success",
                            "reload_type": reload_type,
                            "timestamp": time.time()
                        }
                        self.wfile.write(json.dumps(response_data).encode('utf-8'))
                        
                        print(f"{reload_type} triggered via HTTP POST from {payload.get('file', 'unknown file')}")
                        
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        
                        error_response = {
                            "status": "error",
                            "message": "Invalid JSON"
                        }
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not found')

            def log_message(self, format, *args):
                # Suppress standard HTTP request logging
                pass

        # Store instance for handler
        reload_server_instance = self
        
        # Start the HTTP server
        print(f"Starting HTTP reload server on http://127.0.0.1:{self.port}")
        httpd = HTTPServer(('127.0.0.1', self.port), ReloadHTTPRequestHandler)
        httpd.serve_forever()


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    parser = argparse.ArgumentParser(description='Simple reload server for development')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=35729, help='Port to use (default: 35729)')
    
    args = parser.parse_args()
    
    # Validate host is localhost
    if args.host not in ['127.0.0.1', 'localhost']:
        print("ERROR: Server must bind to 127.0.0.1 only for security")
        return 1

    # Create reload server instance
    server = ReloadServer(port=args.port)

    print(f"HTTP reload server listening on: http://{args.host}:{args.port}/reload")
    print(f"Use this URL to trigger reload: http://{get_local_ip()}:{args.port}/reload")

    # Start server
    server.start()


if __name__ == "__main__":
    main()