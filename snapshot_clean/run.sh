#!/bin/bash

# iPhone Device Frame Tool - Run Script
# This script starts all components of the tool

set -e  # Exit on any error

echo "iPhone Device Frame Tool - Starting"
echo "==================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if required tools are installed
missing_deps=()
if ! command_exists python3; then
    missing_deps+=("python3")
fi

if [ ${#missing_deps[@]} -ne 0 ]; then
    echo "Error: Missing required dependencies: ${missing_deps[*]}"
    echo "Please run: ./install.sh"
    exit 1
fi

# Create auto directory if it doesn't exist
mkdir -p auto

# Start the WebSocket reload server in the background
echo "Starting WebSocket reload server..."
python3 reload_server.py &

# Start the file watcher in the background
echo "Starting file watcher..."
python3 watcher.py &

# Start the device frame application
echo "Starting iPhone Device Frame..."
python3 device_frame.py

echo "Stopping all background processes..."
pkill -f "reload_server.py" || true
pkill -f "watcher.py" || true