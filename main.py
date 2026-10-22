from __future__ import annotations

import asyncio
import logging

from telethon import Button, TelegramClient, events, utils
from telethon.errors import FloodWaitError, RPCError

import config
import notifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("tg_reply_me")

user = TelegramClient(config.USER_SESSION, config.API_ID, config.API_HASH)
bot = TelegramClient(config.BOT_SESSION, config.API_ID, config.API_HASH)

me = None
owner_id = None


async def send_to_owner(text: str, link: str | None) -> None:
    buttons = [Button.url("➡️ Xabarga o'tish", link)] if link else None
    for _ in range(3):
        try:
            await bot.send_message(
                owner_id, text, parse_mode="html", buttons=buttons, link_preview=False
            )
            return
        except FloodWaitError as e:
            log.warning("FloodWait %s s", e.seconds)
            await asyncio.sleep(e.seconds + 1)
        except RPCError as e:
            log.error(
                "Botdan yuborib bo'lmadi (%s). Botga /start bosganingizni tekshiring.", e
            )
            return


@user.on(events.NewMessage(incoming=True))
async def on_message(event: events.NewMessage.Event) -> None:
    if event.is_private:
        return
    msg = event.message
    # Telegram bu flagni @mention, text_mention va xabaringizga reply uchun qo'yadi
    if not msg.mentioned:
        return
    if event.sender_id == me.id or event.chat_id in config.IGNORE_CHATS:
        return

    try:
        chat = await event.get_chat()
        sender = await event.get_sender()

        kind = notifier.KIND_MENTION
        replied_text = None
        if msg.is_reply:
            replied = await event.get_reply_message()
            if replied and replied.sender_id == me.id:
                kind = notifier.KIND_REPLY
                replied_text = replied.raw_text or notifier.media_label(replied)

        chat_username = getattr(chat, "username", None)
        text = notifier.build_notification(
            kind=kind,
            chat_title=utils.get_display_name(chat) or "Noma'lum chat",
            chat_username=chat_username,
            sender_name=utils.get_display_name(sender) if sender else "Noma'lum",
            sender_username=getattr(sender, "username", None),
            sender_id=event.sender_id,
            date=msg.date,
            tz=config.TIMEZONE,
            text=msg.raw_text,
            media=notifier.media_label(msg),
            replied_text=replied_text,
        )
        link = notifier.message_link(event.chat_id, chat_username, msg.id)
    except Exception:
        log.exception("Xabarni qayta ishlashda xato")
        return

    log.info("%s: chat=%s msg=%s", kind, event.chat_id, msg.id)
    await send_to_owner(text, link)


@bot.on(events.NewMessage(pattern="/start", incoming=True))
async def on_start(event: events.NewMessage.Event) -> None:
    if event.sender_id != owner_id:
        await event.reply("Bu shaxsiy bot.")
        return
    await event.reply(
        "Ishlayapman ✅\nGuruhlarda sizni belgilashsa yoki xabaringizga "
        "reply qilishsa, shu yerga yuboraman."
    )


async def main() -> None:
    global me, owner_id

    await user.connect()
    if not await user.is_user_authorized():
        raise SystemExit("Akkaunt sessiyasi topilmadi. Avval: python login.py")
    me = await user.get_me()
    owner_id = config.OWNER_ID or me.id

    await bot.start(bot_token=config.BOT_TOKEN)
    bot_me = await bot.get_me()

    log.info(
        "Ishga tushdi: akkaunt=@%s (%s), bot=@%s, egasi=%s",
        me.username, me.id, bot_me.username, owner_id,
    )
    await asyncio.gather(user.run_until_disconnected(), bot.run_until_disconnected())


if __name__ == "__main__":
    asyncio.run(main())
