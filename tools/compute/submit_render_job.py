#!/usr/bin/env python3
"""Create a durable render job without performing heavy rendering in the API process."""
import argparse,json,time,uuid
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--scene",required=True); ap.add_argument("--blend",required=True); ap.add_argument("--output",required=True); ap.add_argument("--mars-sha256",required=True); ap.add_argument("--seed",required=True); ap.add_argument("--queue",default="artifacts/jobs")
    a=ap.parse_args(); root=Path(a.queue); root.mkdir(parents=True,exist_ok=True)
    job_id=f"GM-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    job={"schema":"trippedd.render-job.v1","job_id":job_id,"scene":a.scene,"blend":str(Path(a.blend).resolve()),"output":str(Path(a.output).resolve()),"mars_sha256":a.mars_sha256,"seed":a.seed,"state":"QUEUED","attempt":0,"created_at":time.time()}
    p=root/f"{job_id}.json"; p.write_text(json.dumps(job,indent=2)+"\n"); print(json.dumps({"job_id":job_id,"state":"QUEUED","job_file":str(p)}))
if __name__=="__main__": main()
