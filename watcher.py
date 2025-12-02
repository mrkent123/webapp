#!/usr/bin/env python3
"""
File Watcher for iPhone Device Frame Tool
Watches for file changes in the ./src directory and sends reload signal to WebSocket server
"""

import time
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import websocket
import threading


class ReloadTrigger:
    def __init__(self, ws_url="ws://localhost:3210"):
        self.ws_url = ws_url
        self.ws = None
        self.connected = False
        
    def connect(self):
        """Attempt to connect to WebSocket server"""
        try:
            # Note: Using a simple approach since we're triggering reloads, not receiving
            # We'll send HTTP requests to the reload endpoint instead of WebSocket
            # because the WebSocket library for Python has some issues with threading
            import urllib.request
            # Test connection by making a simple request to the HTTP reload endpoint
            try:
                urllib.request.urlopen(f"http://localhost:3211/reload")
                print("Successfully connected to reload server")
                return True
            except:
                print("Could not connect to reload server at http://localhost:3211/reload")
                return False
        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")
            return False
    
    def trigger_reload(self):
        """Trigger reload by sending message to WebSocket"""
        try:
            # Use the HTTP endpoint to trigger reload
            import urllib.request
            import urllib.error
            
            req = urllib.request.Request(f"http://localhost:3211/reload")
            urllib.request.urlopen(req)
            print("Reload triggered successfully")
        except urllib.error.URLError as e:
            print(f"Failed to trigger reload: {e}")
        except Exception as e:
            print(f"Error triggering reload: {e}")


class SrcFileHandler(FileSystemEventHandler):
    def __init__(self, reload_trigger):
        super().__init__()
        self.reload_trigger = reload_trigger
        self.last_trigger_time = 0
        self.cooldown_period = 1.0  # 1 second cooldown to prevent multiple triggers
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Check if this is a source file
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() in ['.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.html', '.vue', '.json', '.py']:
            current_time = time.time()
            if current_time - self.last_trigger_time > self.cooldown_period:
                print(f"File changed: {event.src_path}")
                self.reload_trigger.trigger_reload()
                self.last_trigger_time = current_time
    
    def on_created(self, event):
        if event.is_directory:
            return
            
        # Check if this is a source file
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() in ['.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.html', '.vue', '.json', '.py']:
            current_time = time.time()
            if current_time - self.last_trigger_time > self.cooldown_period:
                print(f"File created: {event.src_path}")
                self.reload_trigger.trigger_reload()
                self.last_trigger_time = current_time


def main():
    print("Starting file watcher...")
    
    # Create reload trigger
    reload_trigger = ReloadTrigger()
    
    # Check if we can connect to the reload server
    if not reload_trigger.connect():
        print("Could not connect to reload server. Please make sure reload_server.py is running.")
        sys.exit(1)
    
    # Check if src directory exists
    src_dir = "./src"
    if not os.path.exists(src_dir):
        print(f"Warning: {src_dir} directory does not exist. Creating it...")
        os.makedirs(src_dir, exist_ok=True)
    
    # Create event handler
    event_handler = SrcFileHandler(reload_trigger)
    
    # Create observer
    observer = Observer()
    observer.schedule(event_handler, path=src_dir, recursive=True)
    
    # Start the observer
    observer.start()
    print(f"Watching for changes in: {os.path.abspath(src_dir)}")
    print("Press Ctrl+C to stop watching")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping file watcher...")
    
    observer.join()
    print("File watcher stopped")


if __name__ == "__main__":
    main()