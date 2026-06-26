#!/bin/bash
set -e

REPO="$(cd "$(dirname "$0")" && pwd)"
SERVICE_SRC="$REPO/fika-portal.service"
SERVICE_DEST="/etc/systemd/system/fika-portal.service"

echo "==> Installerar fika-portal.service från $REPO"

# Fyll i sökväg och användare i en temporär kopia
TMP=$(mktemp)
sed -e "s|__REPO__|$REPO|g" \
    -e "s|__USER__|$USER|g" \
    "$SERVICE_SRC" > "$TMP"

sudo cp "$TMP" "$SERVICE_DEST"
rm "$TMP"

sudo chmod +x "$REPO/start_portal.sh"
sudo systemctl daemon-reload
sudo systemctl enable fika-portal
sudo systemctl restart fika-portal

echo ""
echo "==> Status:"
sudo systemctl status fika-portal --no-pager

echo ""
# Visa vilken IP TV:n ska använda
IP=$(hostname -I | awk '{print $1}')
echo "==> Öppna i TV:ns webbläsare: http://$IP:8080/"
