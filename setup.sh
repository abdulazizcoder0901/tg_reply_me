#!/bin/bash
# Birinchi sozlash: .env, kutubxonalar va Telegram sessiyasi. Bor narsani qayta so'ramaydi.
set -e
cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "== Sozlash (bir marta) =="
    read -r -p "API_ID: " API_ID
    read -r -p "API_HASH: " API_HASH
    read -r -p "BOT_TOKEN: " BOT_TOKEN
    cat > .env <<ENV
API_ID=$API_ID
API_HASH=$API_HASH
BOT_TOKEN=$BOT_TOKEN
OWNER_ID=
TIMEZONE=Asia/Tashkent
IGNORE_CHATS=
ENV
    chmod 600 .env
    echo ".env saqlandi"
fi

if [ ! -x .venv/bin/python ]; then
    echo "== Kutubxonalar o'rnatilmoqda (bir marta) =="
    python3 -m venv .venv
    .venv/bin/python -m pip install -q --upgrade pip
fi
.venv/bin/python -m pip install -q -r requirements.txt

if [ ! -f sessions/user.session ]; then
    echo "== Telegram akkauntga kirish (bir marta) =="
    .venv/bin/python login.py
fi
