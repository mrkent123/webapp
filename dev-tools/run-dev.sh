#!/bin/bash

# iPhone Dev Mode Pro Orchestrator
# Starts all required services for development

echo "iPhone Dev Mode Pro Orchestrator Starting..."

# Source Qt environment variables
source /home/mrkent/dev/webapp/qt_env_setup.sh

# Start the reload server (only on 127.0.0.1)
echo "Starting reload server..."
cd /home/mrkent/dev/webapp && /home/mrkent/dev/webapp/.venv/bin/python reload_server.py 127.0.0.1 8080 &

# Start the file watcher
echo "Starting file watcher..."
cd /home/mrkent/dev/webapp && /home/mrkent/dev/webapp/.venv/bin/python watcher.py &

# Start the smart reloader
echo "Starting smart reloader..."
cd /home/mrkent/dev/webapp && /home/mrkent/dev/webapp/.venv/bin/python smart-reloader.py &

# Start the Vite dev server with proper host
echo "Starting Vite dev server..."
cd /home/mrkent/dev/webapp && npx vite --host 127.0.0.1 &

echo "All services started!"
echo "Vite: http://127.0.0.1:5173"
echo "Reload Server: http://127.0.0.1:8080"

# Keep the process running
wait