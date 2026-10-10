#!/usr/bin/env bash
# ONE BLENDER, HELD OPEN.
#
#   "you're wasting my sessions"  -- and he was right: answering one question
#   about his mouth cost TEN Blender launches, each reloading the same scene.
#
#   bash tools/session/start.sh assets/rigs/MARS_FACE.blend
#   ./.trippedd_venv/bin/python tools/session/client.py scene
#
# The session is also what Rocket talks to. Same socket, same live scene: Claude
# inspects and corrects, the human grabs the same object and moves it, and
# neither side reloads anything.
set -euo pipefail
cd "$(dirname "$0")/../.."
BLEND="${1:-assets/rigs/MARS_FACE.blend}"
PORT="${TRIPPEDD_SESSION_PORT:-9876}"
LOG="${TRIPPEDD_SESSION_LOG:-/tmp/trippedd_session_${PORT}.log}"
bash tools/session/provision_session.sh >/dev/null
if ./.trippedd_venv/bin/python tools/session/client.py ping --port "$PORT" >/dev/null 2>&1; then
  echo "session already live on $PORT -- not starting a second one"; exit 0
fi
export TRIPPEDD_ROOT="$PWD" TRIPPEDD_SESSION_PORT="$PORT"
nohup xvfb-run -a vendor/blender/blender "$BLEND" -P tools/session/_boot.py > "$LOG" 2>&1 &
echo "starting session on port $PORT, log $LOG"
for i in $(seq 1 60); do
  grep -q SESSION_READY "$LOG" 2>/dev/null && { grep SESSION_READY "$LOG" | tail -1; exit 0; }
  grep -q SESSION_BOOT_FAIL "$LOG" 2>/dev/null && { grep SESSION_BOOT_FAIL "$LOG" | tail -1; exit 1; }
  sleep 2
done
echo "session did not report ready in 120s -- see $LOG" >&2; tail -20 "$LOG" >&2; exit 1
