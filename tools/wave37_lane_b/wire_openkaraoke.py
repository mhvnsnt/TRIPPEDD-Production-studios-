#!/usr/bin/env python3
"""Wave 37 Lane B — wire OpenKaraoke (karaoke session tool) with a REAL proof.

OpenKaraoke (zaidzaihan/OpenKaraoke): web-based karaoke party solution —
rooms, WebSocket endpoints, playlist management. MIT (catalog: "OpenKaraoke
(zaidzaihan) ✅ MIT", verified 2026-10-08). This wire runs the REAL upstream
backend (FastAPI + WebSocket room manager): shallow-clones the repo at wire
time, starts uvicorn on the real main.py, then drives a REAL session over
HTTP + WebSocket — create room, host join, client join, enqueue 2 songs,
control commands, song-ended auto-advance, comments — recording every message
as a transcript. Assertions verify the room/queue protocol behaved; the
transcript JSON in proofs_openkaraoke/ is the real output.

Self-contained: bootstraps a venv (W37B_VENV, default /tmp/w37b_venv) and
pip-installs fastapi/uvicorn/websockets/youtube-search into it, then re-execs
under that interpreter.

Usage: python3 tools/wave37_lane_b/wire_openkaraoke.py
"""
import asyncio
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WORKDIR = os.path.join(HERE, "proofs_openkaraoke")
VENV = os.environ.get("W37B_VENV", "/tmp/w37b_venv")
REPO_URL = "https://github.com/zaidzaihan/OpenKaraoke.git"
PORT = int(os.environ.get("W37B_OK_PORT", "8471"))

os.makedirs(WORKDIR, exist_ok=True)


def log(msg):
    print(f"[wire_openkaraoke] {msg}", flush=True)


def ensure_env():
    try:
        import fastapi, uvicorn, websockets  # noqa
        return
    except ImportError:
        pass
    py = os.path.join(VENV, "bin", "python")
    if not os.path.exists(py):
        log(f"creating venv at {VENV}")
        subprocess.run([sys.executable, "-m", "venv", VENV], check=True)
        subprocess.run([py, "-m", "pip", "install", "-q",
                        "fastapi", "uvicorn", "websockets", "youtube-search"],
                       check=True)
    log("re-exec under venv python")
    env = dict(os.environ)
    os.execvpe(py, [py, os.path.abspath(__file__)], env)


def clone_backend():
    tmp = os.path.join(os.environ.get("W37B_TMP", "/tmp"), "w37b_openkaraoke_src")
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    log(f"shallow-cloning {REPO_URL}")
    subprocess.run(["git", "clone", "--depth", "1", REPO_URL, tmp],
                   check=True, capture_output=True)
    sha = subprocess.run(["git", "-C", tmp, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return tmp, sha


def wait_port(port, timeout=30):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=2):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def http_get(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}",
                                timeout=15) as r:
        return json.loads(r.read().decode())


async def run_session():
    import websockets
    transcript = []

    def rec(direction, payload):
        transcript.append({"t": round(time.time(), 3), "dir": direction,
                           "msg": payload})

    # 1. create room over HTTP
    room = http_get("/create-room")
    room_id = room["room_id"]
    log(f"room created: {room_id}")
    assert isinstance(room_id, str) and len(room_id) == 6 and room_id.isdigit(), \
        f"room_id not a 6-digit code: {room_id!r}"
    rec("http", {"GET /create-room": room})

    uri = f"ws://127.0.0.1:{PORT}/ws/{room_id}"

    # 2. host joins
    host_ws = await websockets.connect(uri)
    await host_ws.send(json.dumps({"username": "Host", "is_host": True}))
    host_msgs = [json.loads(await host_ws.recv()), json.loads(await host_ws.recv())]
    for m in host_msgs:
        rec("host<-", m)
    assert host_msgs[0]["type"] == "user_joined" and host_msgs[0]["username"] == "Host", host_msgs[0]
    assert host_msgs[1]["type"] == "queue_list" and host_msgs[1]["list"] == [], host_msgs[1]
    log("host joined: user_joined + empty queue_list OK")

    # 3. client joins
    cli_ws = await websockets.connect(uri)
    await cli_ws.send(json.dumps({"username": "Singer1", "is_host": False}))
    cli_join = json.loads(await cli_ws.recv())   # user_joined (own)
    cli_queue = json.loads(await cli_ws.recv())  # queue_list
    host_sees_join = json.loads(await host_ws.recv())  # broadcast user_joined
    for m in (cli_join, cli_queue):
        rec("cli<-", m)
    rec("host<-", host_sees_join)
    assert cli_join["type"] == "user_joined" and cli_join["username"] == "Singer1"
    assert host_sees_join["type"] == "user_joined" and host_sees_join["username"] == "Singer1"
    log("client joined: join broadcast seen by host OK")

    song_a = {"title": "Bohemian Rhapsody (Karaoke)",
              "url": "https://www.youtube.com/watch?v=testAAA",
              "duration": "5:55"}
    song_b = {"title": "Sweet Caroline (Karaoke)",
              "url": "https://www.youtube.com/watch?v=testBBB",
              "duration": "3:21"}

    async def drain(ws, n, tag):
        out = []
        for _ in range(n):
            m = json.loads(await asyncio.wait_for(ws.recv(), timeout=10))
            out.append(m)
            rec(tag, m)
        return out

    # 4. client enqueues song A -> queue_list + auto-play control
    await cli_ws.send(json.dumps({"type": "queue_update", "song": song_a}))
    rec("cli->", {"type": "queue_update", "song": song_a["title"]})
    h1 = await drain(host_ws, 2, "host<-")
    c1 = await drain(cli_ws, 2, "cli<-")
    ql = [m for m in h1 if m["type"] == "queue_list"][0]
    play = [m for m in h1 if m.get("type") == "control" and m.get("command") == "Play"][0]
    assert len(ql["list"]) == 1 and ql["list"][0]["song"]["title"] == song_a["title"], ql
    assert ql["list"][0]["added_by"] == "Singer1", ql
    assert play["song"]["title"] == song_a["title"], play
    log("enqueue A: queue_list(1) + auto-Play broadcast OK")

    # 5. client enqueues song B -> queue_list only (no auto-play)
    await cli_ws.send(json.dumps({"type": "queue_update", "song": song_b}))
    rec("cli->", {"type": "queue_update", "song": song_b["title"]})
    h2 = await drain(host_ws, 1, "host<-")
    c2 = await drain(cli_ws, 1, "cli<-")
    ql2 = h2[0]
    assert ql2["type"] == "queue_list" and len(ql2["list"]) == 2, ql2
    assert ql2["list"][1]["song"]["title"] == song_b["title"], ql2
    log("enqueue B: queue_list(2), no auto-play OK")

    # 6. host reports song ended -> queue advances, song B auto-plays
    await host_ws.send(json.dumps({"type": "song_ended"}))
    rec("host->", {"type": "song_ended"})
    h3 = await drain(host_ws, 2, "host<-")
    c3 = await drain(cli_ws, 2, "cli<-")
    ql3 = [m for m in h3 if m["type"] == "queue_list"][0]
    play3 = [m for m in h3 if m.get("type") == "control" and m.get("command") == "Play"][0]
    assert len(ql3["list"]) == 1 and ql3["list"][0]["song"]["title"] == song_b["title"], ql3
    assert play3["song"]["title"] == song_b["title"], play3
    log("song_ended: queue advanced to B + auto-Play B OK")

    # 7. comment broadcast
    await cli_ws.send(json.dumps({"type": "comment", "comment": "Great pick!"}))
    rec("cli->", {"type": "comment", "comment": "Great pick!"})
    hc = await drain(host_ws, 1, "host<-")
    cc = await drain(cli_ws, 1, "cli<-")
    assert hc[0]["type"] == "comment" and hc[0]["comment"] == "Great pick!" \
        and hc[0]["username"] == "Singer1", hc[0]
    log("comment broadcast OK")

    # 8. control Pause broadcast
    await host_ws.send(json.dumps({"type": "control", "command": "Pause"}))
    rec("host->", {"type": "control", "command": "Pause"})
    hp = await drain(host_ws, 1, "host<-")
    cp = await drain(cli_ws, 1, "cli<-")
    assert hp[0]["type"] == "control" and hp[0]["command"] == "Pause", hp[0]
    log("control Pause broadcast OK")

    await host_ws.close()
    await cli_ws.close()
    return room_id, transcript


def main():
    ensure_env()
    src, sha = clone_backend()
    log(f"upstream HEAD {sha}")

    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=os.path.join(src, "backend"),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        assert wait_port(PORT), "uvicorn did not come up"
        log(f"uvicorn up on 127.0.0.1:{PORT}")
        room_id, transcript = asyncio.run(run_session())
    finally:
        server.terminate()
        try:
            out, _ = server.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            out = ""
        with open(os.path.join(WORKDIR, "uvicorn.log"), "w") as f:
            f.write(out or "")

    proof = {
        "tool": "OpenKaraoke",
        "tool_version": f"upstream git HEAD {sha}",
        "tool_license": "MIT (catalog: OpenKaraoke (zaidzaihan) ✅ MIT, verified 2026-10-08)",
        "repo": REPO_URL,
        "run": {"port": PORT, "room_id": room_id,
                "server": "real uvicorn + FastAPI backend (main.py + rooms.py, unmodified upstream)",
                "messages": len(transcript)},
        "checks": [
            "room_id is a 6-digit code",
            "host join -> user_joined broadcast + empty queue_list",
            "client join -> user_joined broadcast seen by host",
            "enqueue song A -> queue_list(1) with added_by=Singer1 + auto-Play broadcast",
            "enqueue song B -> queue_list(2), no auto-play",
            "song_ended -> queue advances to song B + auto-Play B broadcast",
            "comment -> comment broadcast to all clients",
            "control Pause -> control broadcast to all clients",
        ],
        "transcript": "openkaraoke_transcript.json",
        "ran": "2026-10-08",
    }
    with open(os.path.join(WORKDIR, "openkaraoke_transcript.json"), "w") as f:
        json.dump(transcript, f, indent=2)
    with open(os.path.join(WORKDIR, "openkaraoke_proof.json"), "w") as f:
        json.dump(proof, f, indent=2)
    log(f"transcript: {len(transcript)} messages -> {WORKDIR}/openkaraoke_transcript.json")
    log("DONE — OpenKaraoke wired with real proof")


if __name__ == "__main__":
    main()
