#!/usr/bin/env python3
"""Durable, authenticated webhook/reconciliation supervisor for TRIPPEDD JIT runners."""
from __future__ import annotations
import hashlib,hmac,json,os,pathlib,subprocess,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

ROOT=pathlib.Path(os.environ.get("TRIPPEDD_STATE_DIR","/var/lib/trippedd-production"))
ROOT.mkdir(parents=True,exist_ok=True)
STATE=ROOT/"autonomous-state.json"
EVENTS=ROOT/"autonomous-events.jsonl"
LOCK=threading.Lock()

def load():
    try:return json.loads(STATE.read_text())
    except FileNotFoundError:return {"active_jobs":{},"deliveries":{}}

def save(s):
    tmp=STATE.with_suffix(".tmp"); tmp.write_text(json.dumps(s,indent=2)); os.replace(tmp,STATE)

def event(kind,payload):
    with EVENTS.open("a") as f:f.write(json.dumps({"ts":time.time(),"kind":kind,"payload":payload})+"\n")

def valid_signature(body,signature,secret):
    if not signature or not secret:return False
    mac=hmac.new(secret.encode(),body,hashlib.sha256).hexdigest()
    return hmac.compare_digest("sha256="+mac,signature)

def provision(job):
    jid=str(job["id"])
    with LOCK:
        s=load()
        if jid in s["active_jobs"]: return
        s["active_jobs"][jid]={"status":"provisioning","updated":time.time()}
        save(s); event("provision_requested",{"job_id":jid,"run_id":job.get("run_id")})
    env=os.environ.copy()
    env["TRIPPEDD_GITHUB_OWNER"]=job["repository"]["owner"]["login"]
    env["TRIPPEDD_GITHUB_REPO"]=job["repository"]["name"]
    env["TRIPPEDD_RUNNER_NAME"]=f"trippedd-jit-{jid}"
    try:
        subprocess.Popen(["python3","-m","github_app.jit_runner"],env=env,
                         stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
    except Exception as e:
        with LOCK:
            s=load(); s["active_jobs"][jid]={"status":"failed_to_spawn","error":str(e),"updated":time.time()}; save(s)
        event("provision_failed",{"job_id":jid,"error":str(e)})

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body=self.rfile.read(int(self.headers.get("Content-Length","0")))
        if not valid_signature(body,self.headers.get("X-Hub-Signature-256",""),os.environ.get("TRIPPEDD_WEBHOOK_SECRET","")):
            self.send_response(401); self.end_headers(); return
        if self.headers.get("X-GitHub-Event")!="workflow_job":
            self.send_response(204); self.end_headers(); return
        delivery=self.headers.get("X-GitHub-Delivery","")
        if not delivery:
            self.send_response(400); self.end_headers(); return
        payload=json.loads(body)
        repo=payload.get("repository",{}).get("full_name","")
        allowed=os.environ.get("TRIPPEDD_ALLOWED_REPOSITORY","")
        if allowed and repo.lower()!=allowed.lower():
            self.send_response(204); self.end_headers(); return
        action=payload.get("action")
        job=payload.get("workflow_job",{})
        with LOCK:
            s=load()
            if delivery in s.setdefault("deliveries",{}):
                self.send_response(202); self.end_headers(); return
            s["deliveries"][delivery]={"ts":time.time(),"action":action}
            s["deliveries"]={k:v for k,v in s["deliveries"].items() if time.time()-v["ts"]<86400}
            save(s)
        labels={x.get("name") for x in job.get("labels",[])}
        wanted=os.environ.get("TRIPPEDD_RUNNER_LABEL","trippedd-production")
        if action=="queued" and wanted in labels:
            threading.Thread(target=provision,args=(job,),daemon=True).start()
        self.send_response(202); self.end_headers()
    def log_message(self,*args): pass

def main():
    host=os.environ.get("TRIPPEDD_BIND","127.0.0.1")
    port=int(os.environ.get("TRIPPEDD_PORT","8099"))
    event("supervisor_started",{"host":host,"port":port})
    ThreadingHTTPServer((host,port),Handler).serve_forever()

if __name__=="__main__":main()
