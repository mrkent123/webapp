#!/usr/bin/env python3
import json, os, sys, subprocess

WS = os.environ["WORKSPACE"]
profile_path = os.path.join(WS, "dev-tools", "device-profile.json")

with open(profile_path) as f:
    profile = json.load(f)

url = sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:5173"
env = os.environ.copy()

env["DEVICE_DPR"] = str(profile["dpr"])
env["DEVICE_VIEW_W"] = str(profile["viewport_css"]["width"])
env["DEVICE_VIEW_H"] = str(profile["viewport_css"]["height"])
env["DEVICE_UA"] = profile["user_agent"]

cmd = ["python3", os.path.join(WS, "device_frame.py"), url]
subprocess.Popen(cmd, env=env)