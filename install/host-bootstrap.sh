#!/usr/bin/env bash
set -euo pipefail

: "${TRIPPEDD_RUNNER_VERSION:?Set a pinned actions-runner version}"
: "${TRIPPEDD_INSTALL_DIR:=/opt/trippedd-runner}"
: "${TRIPPEDD_SERVICE_USER:=trippedd}"

id "$TRIPPEDD_SERVICE_USER" >/dev/null 2>&1 || sudo useradd --system --create-home --shell /usr/sbin/nologin "$TRIPPEDD_SERVICE_USER"
sudo install -d -o "$TRIPPEDD_SERVICE_USER" -g "$TRIPPEDD_SERVICE_USER" "$TRIPPEDD_INSTALL_DIR"

arch="$(uname -m)"
case "$arch" in
  x86_64) asset="actions-runner-linux-x64-${TRIPPEDD_RUNNER_VERSION}.tar.gz" ;;
  aarch64|arm64) asset="actions-runner-linux-arm64-${TRIPPEDD_RUNNER_VERSION}.tar.gz" ;;
  *) echo "Unsupported architecture: $arch" >&2; exit 2 ;;
esac

url="https://github.com/actions/runner/releases/download/v${TRIPPEDD_RUNNER_VERSION}/${asset}"
tmp="$(mktemp)"
curl -fsSL "$url" -o "$tmp"
sudo tar -xzf "$tmp" -C "$TRIPPEDD_INSTALL_DIR"
rm -f "$tmp"
sudo chown -R "$TRIPPEDD_SERVICE_USER:$TRIPPEDD_SERVICE_USER" "$TRIPPEDD_INSTALL_DIR"

python3 -m pip install --upgrade PyJWT cryptography

sudo install -d -m 0750 /etc/trippedd
sudo chown "$TRIPPEDD_SERVICE_USER:$TRIPPEDD_SERVICE_USER" /etc/trippedd

echo "Runner binaries installed. Supply GitHub App credentials through the host secret manager, then start the supervisor."
