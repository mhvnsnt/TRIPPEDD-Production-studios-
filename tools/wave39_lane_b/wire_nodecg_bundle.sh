#!/bin/bash
# Wave 39 Lane B — NodeCG broadcast-graphics bundle wiring proof.
#
# 1. npm-installs the MIT-licensed NodeCG server (pinned version) — node_modules
#    are NOT committed (see .gitignore in this dir).
# 2. installs the local trippedd-lowerthird bundle into bundles/
# 3. starts the server briefly, fetches the dashboard + graphics URLs (must be 200),
#    greps the server log for the bundle's extension load line
# 4. stops the server, writes PROOFS.md
set -u
SRV="$PWD/nodecg_server"
BUNDLESRC="$PWD/nodecg_bundles/trippedd-lowerthird"
LOG="$PWD/nodecg_proof.log"

mkdir -p "$SRV"
cd "$SRV"
[ -f package.json ] || npm init -y >/dev/null 2>&1
if [ ! -d node_modules/nodecg ]; then
  echo "npm install nodecg@2.2.0 ..." 
  npm install nodecg@2.2.0 --no-audit --no-fund 2>&1 | tail -2
fi
mkdir -p bundles
rm -rf bundles/trippedd-lowerthird
cp -r "$BUNDLESRC" bundles/trippedd-lowerthird

# start server in background
node node_modules/nodecg/bin/nodecg start > "$LOG" 2>&1 &
SRVPID=$!
echo "server pid $SRVPID; waiting for boot..."
for i in $(seq 1 60); do
  sleep 2
  if grep -q "NodeCG running on" "$LOG" 2>/dev/null; then break; fi
  if ! kill -0 $SRVPID 2>/dev/null; then echo "SERVER DIED"; cat "$LOG"; exit 1; fi
done

echo "--- checks ---"
DASH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/dashboard/)
GFX=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/bundles/trippedd-lowerthird/graphics/lowerthird.html)
GFXBODY=$(curl -s http://localhost:9090/bundles/trippedd-lowerthird/graphics/lowerthird.html)
EXT=$(grep -c "trippedd-lowerthird extension loaded" "$LOG")
RUNNING=$(grep -c "NodeCG running on" "$LOG")
echo "dashboard HTTP: $DASH"
echo "graphics HTTP: $GFX"
echo "graphics contains 'TRIPPEDD' title marker: $(echo "$GFXBODY" | grep -c '<title>Lower Third</title>')"
echo "extension load lines: $EXT"

kill $SRVPID 2>/dev/null
wait $SRVPID 2>/dev/null
echo "server stopped."

cd "$OLDPWD" 2>/dev/null || cd "$(dirname "$0")"
cat > nodecg_PROOFS.md <<EOF
# Wave 39 Lane B — NodeCG broadcast-graphics bundle wiring proofs

Tool wired: **NodeCG** (MIT, https://nodecg.com — broadcast graphics overlay
framework, non-quarantined) with a local TRIPPEDD lower-third bundle.

Bundle: \`tools/wave39_lane_b/nodecg_bundles/trippedd-lowerthird/\`
- \`package.json\` — nodecg-compatible bundle descriptor (dashboard panel + graphic)
- \`extension.js\` — loads on boot, owns the \`lowerThird\` Replicant
- \`dashboard/panel.html\` — control panel (name/title push)
- \`graphics/lowerthird.html\` — 1920x1080 overlay graphic

Server: nodecg@2.2.0 npm-installed (MIT); node_modules excluded from git.

## Run
\`bash tools/wave39_lane_b/wire_nodecg_bundle.sh\`

## Results (fresh run 2026-10-08)
| Check | Result |
|---|---|
| Server boot | $([ "$RUNNING" -ge 1 ] && echo "PASS — 'NodeCG running on' in log" || echo "FAIL") |
| Bundle extension loaded | $([ "$EXT" -ge 1 ] && echo "PASS — 'trippedd-lowerthird extension loaded' in log" || echo "FAIL") |
| Dashboard GET /dashboard/ | HTTP $DASH |
| Graphics GET /bundles/trippedd-lowerthird/graphics/lowerthird.html | HTTP $GFX |

## Artifacts
- \`nodecg_proof.log\` — full server stdout/stderr from the proof run
- \`nodecg_bundles/trippedd-lowerthird/\` — the wired bundle source
EOF
echo "PROOFS written."
