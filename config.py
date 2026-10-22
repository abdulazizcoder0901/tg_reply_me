from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = Path(os.getenv("SESSIONS_DIR", BASE_DIR / "sessions"))
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def _require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        sys.exit(f"[config] {name} .env faylida ko'rsatilmagan")
    return value


def _int_list(raw: str) -> set[int]:
    return {int(x) for x in raw.replace(" ", "").split(",") if x}


API_ID = int(_require("API_ID"))
API_HASH = _require("API_HASH")
BOT_TOKEN = _require("BOT_TOKEN")

# Xabarnoma kimga yuborilsin. Bo'sh bo'lsa — userbot akkauntining o'zi.
OWNER_ID = int(os.getenv("OWNER_ID") or 0) or None

TIMEZONE = os.getenv("TIMEZONE", "Asia/Tashkent")
SESSION_NAME = os.getenv("SESSION_NAME", "user")
IGNORE_CHATS = _int_list(os.getenv("IGNORE_CHATS", ""))

USER_SESSION = str(SESSIONS_DIR / SESSION_NAME)
BOT_SESSION = str(SESSIONS_DIR / "bot")
