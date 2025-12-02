#!/usr/bin/env python3
import sys, json, requests, os

RELOAD_PORT = os.environ.get("RELOAD_PORT","35729")
f = sys.argv[1] if len(sys.argv)>1 else ""

payload = {"type": "HMR"} if f.endswith(".js") else {"type": "FULL_RELOAD"}

try:
  requests.post(f"http://127.0.0.1:{RELOAD_PORT}/reload",
                json=payload, timeout=1)
except Exception as e:
  print("[smart-reloader] Error:", e)