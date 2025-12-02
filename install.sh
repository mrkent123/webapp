#!/bin/bash

# iPhone Device Frame Tool - Installation Script
# This script installs all necessary dependencies for the tool

set -e  # Exit on any error

echo "iPhone Device Frame Tool - Installation"
echo "======================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking for required dependencies..."

# Install system packages
echo "Installing system packages..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm python3-pyqt5 python3-pyqt5.qtwebengine

# Install Python packages
echo "Installing Python packages..."
pip3 install --user websocket-server watchdog

# Create auto directory if it doesn't exist
mkdir -p auto

echo "Installation completed successfully!"
echo ""
echo "To run the iPhone Device Frame Tool:"
echo "  1. Make the run script executable: chmod +x run.sh"
echo "  2. Run the tool: ./run.sh"