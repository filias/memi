#!/usr/bin/env bash
# Run this on a fresh Hetzner VPS (Ubuntu/Debian) as root.
# Usage: bash setup.sh memi.yourdomain.com
set -euo pipefail

DOMAIN="${1:?Usage: bash setup.sh memi.yourdomain.com}"

# Install Caddy
apt-get update
apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
apt-get update
apt-get install -y caddy

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create app user and directory
useradd --system --create-home --shell /usr/sbin/nologin memi || true
mkdir -p /opt/memi
chown memi:memi /opt/memi

# Clone and install
git clone https://github.com/filias/memi.git /opt/memi
cd /opt/memi
uv sync
chown -R memi:memi /opt/memi

# Configure Caddy
cat > /etc/caddy/Caddyfile <<EOF
${DOMAIN} {
    reverse_proxy localhost:8080
}
EOF
systemctl restart caddy

# Configure systemd service
cp deploy/memi.service /etc/systemd/system/memi.service
systemctl daemon-reload
systemctl enable --now memi

echo ""
echo "Done! Point your DNS A record for ${DOMAIN} to this server's IP."
echo "Caddy will automatically get an SSL certificate once DNS propagates."
