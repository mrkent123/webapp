import os, json, time

ws=os.environ["WORKSPACE"]
out={ "workspace":ws, "time":time.ctime(), "logs":{} }

for x in ["vite.log","reload.log","watcher.log","device.log"]:
  p=os.path.join(ws,"dev-tools",x)
  if os.path.exists(p):
    with open(p) as f: out["logs"][x] = f.read()[:2000]

with open(os.path.join(ws,"qwen_run_summary.json"),"w") as f:
  json.dump(out,f,indent=2)

print("[INFO] Summary saved.")