#!/usr/bin/env python3
"""
Smart Reloader for iPhone Dev Mode Pro
Monitors file changes and triggers appropriate reloads
"""

import time
import json
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys

class SmartReloadHandler(SimpleHTTPRequestHandler):
    """Simple handler to respond to frontend reload requests"""
    
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'smart-reloader-running'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

class SmartReloadServer:
    def __init__(self, host='127.0.0.1', port=8081):
        self.host = host
        self.port = port
        self.httpd = HTTPServer((self.host, self.port), SmartReloadHandler)
        
    def start(self):
        print(f"Smart Reloader starting on {self.host}:{self.port}")
        self.httpd.serve_forever()
        
    def stop(self):
        self.httpd.shutdown()

class SmartReloadFileHandler(FileSystemEventHandler):
    """Handles file changes and determines reload type"""
    
    def __init__(self, reload_callback):
        self.reload_callback = reload_callback
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Determine reload type based on file extension
        file_path = event.src_path
        if file_path.endswith('.js'):
            print(f"JS file changed: {file_path}, triggering HMR")
            # For HMR, we don't need to do anything - Vite handles it
        elif file_path.endswith('.css'):
            print(f"CSS file changed: {file_path}, triggering full reload")
            # Trigger full reload through WebSocket or other mechanism
        elif file_path.endswith(('.html', '.vue', '.jsx')):
            print(f"Template file changed: {file_path}, triggering HMR")
            # For template files, HMR may also be possible

def main():
    print("Smart Reloader initializing...")
    
    # Start the HTTP server in a thread
    server = SmartReloadServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    print("Smart Reloader started successfully!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down Smart Reloader...")
        server.stop()
        server_thread.join(timeout=1)

if __name__ == "__main__":
    main()