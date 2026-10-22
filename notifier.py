"""Xabarnoma matnini yasash. Telethon'ga bog'liq emas — test qilish oson."""

from __future__ import annotations

from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

MAX_TEXT = 3500
MAX_QUOTE = 300

KIND_REPLY = "reply"
KIND_MENTION = "mention"

# (Telethon Message atributi, ko'rinadigan belgi) — tartib muhim: gif/video/voice
# ham document hisoblanadi, shuning uchun document oxirida.
_MEDIA = (
    ("photo", "🖼 Rasm"),
    ("sticker", "🎭 Stiker"),
    ("gif", "🎞 GIF"),
    ("video_note", "⏺ Video xabar"),
    ("video", "🎬 Video"),
    ("voice", "🎤 Ovozli xabar"),
    ("audio", "🎵 Audio"),
    ("poll", "📊 So'rovnoma"),
    ("contact", "👤 Kontakt"),
    ("geo", "📍 Joylashuv"),
    ("document", "📎 Fayl"),
)


def media_label(message) -> str | None:
    for attr, label in _MEDIA:
        if getattr(message, attr, None):
            return label
    return None


def message_link(chat_id: int, chat_username: str | None, msg_id: int) -> str | None:
    """Xabarga havola. Oddiy (basic) guruhlar uchun havola yo'q."""
    if chat_username:
        return f"https://t.me/{chat_username}/{msg_id}"
    s = str(chat_id)
    if s.startswith("-100"):
        return f"https://t.me/c/{s[4:]}/{msg_id}"
    return None


def shorten(text: str, limit: int) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def format_time(date: datetime, tz: str) -> str:
    return date.astimezone(ZoneInfo(tz)).strftime("%d.%m.%Y %H:%M:%S")


def build_notification(
    *,
    kind: str,
    chat_title: str,
    chat_username: str | None,
    sender_name: str,
    sender_username: str | None,
    sender_id: int | None,
    date: datetime,
    tz: str,
    text: str,
    media: str | None = None,
    replied_text: str | None = None,
) -> str:
    header = (
        "↩️ <b>Xabaringizga javob berishdi</b>"
        if kind == KIND_REPLY
        else "🔔 <b>Sizni belgilashdi</b>"
    )

    where = f"<b>{escape(chat_title)}</b>"
    if chat_username:
        where += f" (@{escape(chat_username)})"

    who = escape(sender_name)
    if sender_id and sender_id > 0:
        who = f'<a href="tg://user?id={sender_id}">{who}</a>'
    if sender_username:
        who += f" (@{escape(sender_username)})"
    if sender_id:
        who += f" · <code>{sender_id}</code>"

    lines = [
        header,
        "",
        f"📍 <b>Qayerda:</b> {where}",
        f"👤 <b>Kim:</b> {who}",
        f"🕒 <b>Soat:</b> {format_time(date, tz)}",
    ]

    if replied_text:
        lines.append(f"↪️ <b>Sizning xabaringiz:</b> <i>{escape(shorten(replied_text, MAX_QUOTE))}</i>")

    body = []
    if media:
        body.append(f"[{media}]")
    if text:
        body.append(escape(shorten(text, MAX_TEXT)))
    lines += ["", "💬 <b>Xabar:</b>", "\n".join(body) or "<i>(matn yo'q)</i>"]

    return "\n".join(lines)
