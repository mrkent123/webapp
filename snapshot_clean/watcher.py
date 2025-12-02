#!/usr/bin/env python3
"""
File Watcher for iPhone Device Frame Tool with Smart Reloading
Watches for file changes and uses smart reloading based on file type
"""

import time
import sys
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import urllib.request
import urllib.error


class SmartReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_port=35729):
        super().__init__()
        self.reload_port = reload_port
        self.last_trigger_time = 0
        self.cooldown_period = 1.0  # 1 second cooldown to prevent multiple triggers

    def on_modified(self, event):
        if event.is_directory:
            return

        # Check if this is a source file
        _, ext = os.path.splitext(event.src_path)
        filename = os.path.basename(event.src_path)
        
        if ext.lower() in ['.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.html', '.vue', '.json', '.py', '.md']:
            current_time = time.time()
            if current_time - self.last_trigger_time > self.cooldown_period:
                print(f"File changed: {event.src_path}")
                
                # Determine reload type based on file extension
                if ext.lower() == '.js':
                    reload_type = "HMR"
                    print(f"Detected JS file change - using {reload_type} approach")
                elif ext.lower() in ['.css', '.html'] or filename in ['manifest.json', 'serviceWorker.js', 'service-worker.js']:
                    reload_type = "FULL_RELOAD"
                    print(f"Detected HTML/CSS/PWA file change - using {reload_type}")
                
                # Use the smart reloader script
                try:
                    # Call the smart reloader script with the file path
                    subprocess.run(['python3', 'dev-tools/smart-reloader.py', event.src_path], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Smart reloader failed: {e}")
                
                # Fallback: directly trigger reload via HTTP
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:{self.reload_port}/reload")
                    print(f"Fallback reload triggered successfully on port {self.reload_port}")
                except urllib.error.URLError as e:
                    print(f"Failed to trigger fallback reload: {e}")
                
                self.last_trigger_time = current_time

    def on_created(self, event):
        if event.is_directory:
            return

        # Check if this is a source file
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() in ['.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.html', '.vue', '.json', '.py', '.md']:
            current_time = time.time()
            if current_time - self.last_trigger_time > self.cooldown_period:
                print(f"File created: {event.src_path}")
                
                # Use the smart reloader script
                try:
                    subprocess.run(['python3', 'dev-tools/smart-reloader.py', event.src_path], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Smart reloader failed: {e}")
                
                # Fallback: directly trigger reload via HTTP
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:{self.reload_port}/reload")
                    print(f"Fallback reload triggered successfully on port {self.reload_port}")
                except urllib.error.URLError as e:
                    print(f"Failed to trigger fallback reload: {e}")
                
                self.last_trigger_time = current_time


def main():
    # Get port from environment variable or use default
    reload_port = int(os.environ.get('RELOAD_PORT', 35729))
    
    print(f"Starting file watcher with smart reloading on port {reload_port}...")

    # Verify reload server is running
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{reload_port}/reload")
        print(f"Verified connection to reload server at http://127.0.0.1:{reload_port}/reload")
    except urllib.error.URLError:
        print(f"Warning: Could not connect to reload server. Please make sure reload_server.py is running on port {reload_port}.")

    # Watch the current directory and subdirectories
    watch_dir = "."

    # Create event handler with the correct port
    event_handler = SmartReloadHandler(reload_port=reload_port)

    # Create observer
    observer = Observer()
    observer.schedule(event_handler, path=watch_dir, recursive=True)

    # Start the observer
    observer.start()
    print(f"Watching for changes in: {os.path.abspath(watch_dir)} recursively")
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