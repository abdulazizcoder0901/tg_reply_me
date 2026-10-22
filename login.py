"""Birinchi marta akkauntga kirish: telefon raqam, kod va (bo'lsa) 2FA parol."""

import asyncio

from telethon import TelegramClient

import config


async def main() -> None:
    client = TelegramClient(config.USER_SESSION, config.API_ID, config.API_HASH)
    await client.start()
    me = await client.get_me()
    print(f"Kirildi: {me.first_name} (@{me.username}, id={me.id})")
    print(f"Sessiya saqlandi: {config.USER_SESSION}.session")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
