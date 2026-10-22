#!/bin/bash
# Ubuntu serverga (masalan Oracle Cloud Free) o'rnatish va 24/7 ishga tushirish.
# Qayta ishga tushirilsa — kodni yangilaydi va xizmatni qayta yoqadi.
#
#   bash <(curl -fsSL https://raw.githubusercontent.com/abdulazizcoder0901/tg_reply_me/claude/affectionate-cerf-k66w38/deploy/install.sh)
set -e
REPO="${REPO:-https://github.com/abdulazizcoder0901/tg_reply_me.git}"
BRANCH="${BRANCH:-claude/affectionate-cerf-k66w38}"
DIR="${DIR:-$HOME/tg_reply_me}"
SERVICE=tg_reply_me

echo "== Kerakli dasturlar o'rnatilmoqda =="
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git python3 python3-venv >/dev/null

if [ -d "$DIR/.git" ]; then
    echo "== Kod yangilanmoqda =="
    git -C "$DIR" pull -q --ff-only
else
    echo "== Kod yuklanmoqda =="
    git clone -q -b "$BRANCH" "$REPO" "$DIR"
fi

bash "$DIR/setup.sh"

echo "== Doimiy xizmat sozlanmoqda =="
sudo tee /etc/systemd/system/$SERVICE.service >/dev/null <<UNIT
[Unit]
Description=tg_reply_me (mention/reply notifier)
After=network-online.target
Wants=network-online.target

[Service]
User=$(id -un)
WorkingDirectory=$DIR
ExecStart=$DIR/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload
sudo systemctl enable -q $SERVICE
sudo systemctl restart $SERVICE
sleep 5
sudo systemctl --no-pager --lines=5 status $SERVICE || true

echo
echo "Tayyor ✅ Bot serverda 24/7 ishlayapti."
echo "Loglar:      sudo journalctl -u $SERVICE -f"
echo "To'xtatish:  sudo systemctl stop $SERVICE"
