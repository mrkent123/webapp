#!/usr/bin/env bash
set -e

WORKSPACE="${WORKSPACE:?}"
export VITE_PORT=5173
export VITE_HOST="127.0.0.1"
export RELOAD_PORT=35729

cd "$WORKSPACE"

# Activate virtual environment
source .venv/bin/activate

echo "[RUNDEV] Starting reload_server..."
python3 reload_server.py --host 127.0.0.1 --port $RELOAD_PORT > dev-tools/reload.log 2>&1 &
PID_RELOAD=$!

echo "[RUNDEV] Starting watcher..."
python3 watcher.py > dev-tools/watcher.log 2>&1 &
PID_WATCH=$!

echo "[RUNDEV] Starting Vite..."
npm run dev -- --host 127.0.0.1 --port $VITE_PORT > dev-tools/vite.log 2>&1 &
PID_VITE=$!

echo "[RUNDEV] Starting device frame..."
python3 dev-tools/device-frame-wrapper.py "http://127.0.0.1:$VITE_PORT" > dev-tools/device.log 2>&1 &

sleep 10

echo "[RUNDEV] Checking ports:"
ss -ltnp | grep -E "$PID_RELOAD|$PID_VITE" || true

echo "[RUNDEV] HMR test"
touch js/hmr_test.js

sleep 2

echo "[RUNDEV] FULL reload test"
touch pages/reload_test.html

sleep 2

echo "[RUNDEV] Cleanup"
kill $PID_RELOAD $PID_WATCH $PID_VITE 2>/dev/null || true