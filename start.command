#!/bin/bash
# Mac'da bitta buyruq bilan ishga tushirish: bash start.command
set -e
cd "$(dirname "$0")"
bash setup.sh

echo "== Ishga tushdi. To'xtatish uchun: Ctrl + C =="
exec .venv/bin/python main.py
