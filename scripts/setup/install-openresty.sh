#!/usr/bin/env bash
set -euo pipefail

# One-click OpenResty installer for Ubuntu (22.04/20.04).

if [ "$(id -u)" -ne 0 ]; then
  echo "[ERROR] Please run as root (sudo)."
  exit 1
fi

echo "[INFO] Installing dependencies..."
apt-get update -y
apt-get install -y --no-install-recommends \
  curl ca-certificates gnupg lsb-release \
  build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev

echo "[INFO] Adding OpenResty APT repo..."
curl -fsSL https://openresty.org/package/pubkey.gpg | gpg --dearmor -o /usr/share/keyrings/openresty.gpg
echo "deb [signed-by=/usr/share/keyrings/openresty.gpg] http://openresty.org/package/ubuntu $(lsb_release -sc) main" \
  | tee /etc/apt/sources.list.d/openresty.list > /dev/null

echo "[INFO] Installing OpenResty..."
apt-get update -y
apt-get install -y openresty

echo "[INFO] Enabling OpenResty service..."
systemctl enable openresty
systemctl start openresty

echo "[INFO] OpenResty installed."
echo "Config path: /usr/local/openresty/nginx/conf/nginx.conf"
echo "Vhost dir:   /usr/local/openresty/nginx/conf/conf.d"
