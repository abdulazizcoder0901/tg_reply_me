# tg_reply_me

Telegram'ni doim tekshirib o'tirmaslik uchun: guruhlarda (va kanal komentariyalarida) sizni
**@username bilan belgilashsa** yoki **xabaringizga reply qilishsa**, shaxsiy botingiz sizga yozadi:

```
↩️ Xabaringizga javob berishdi

📍 Qayerda: Dasturchilar (@dev_uz)
👤 Kim: Ali Valiyev (@ali) · 12345
🕒 Soat: 22.10.2026 12:30:15
↪️ Sizning xabaringiz: kecha deploy qildingmi?

💬 Xabar:
Ha, hammasi ishlayapti 👍
                       [➡️ Xabarga o'tish]
```

## Qanday ishlaydi

Oddiy bot begona guruhlardagi xabarlarni ko'ra olmaydi, shuning uchun ikki qism bor:

- **Userbot** (Telethon, sizning akkauntingiz sessiyasi) — barcha guruhlardagi xabarlarni tinglaydi.
  Telegram o'zi belgilaydigan `mentioned` flagi orqali @mention, username'siz belgilash va sizga
  qilingan reply'larni ajratadi.
- **Bot** (@BotFather token) — topilgan xabar haqida sizga xabarnoma yuboradi.

Shaxsiy chatlar kuzatilmaydi — faqat guruh, supergroup va kanal komentariyalari.

## Sozlash

1. **API_ID / API_HASH**: https://my.telegram.org → *API development tools* → ilova yarating.
2. **BOT_TOKEN**: @BotFather → `/newbot`. So'ng yangi botingizga kirib **/start** bosing
   (aks holda bot sizga yoza olmaydi).
3. `.env` yarating:
   ```bash
   cp .env.example .env
   # API_ID, API_HASH, BOT_TOKEN ni to'ldiring
   ```
   `OWNER_ID` bo'sh qolsa, xabarnomalar userbot akkauntining o'ziga keladi.
   `IGNORE_CHATS` — xabarnoma kerak bo'lmagan chatlar ID lari (vergul bilan).

## Ishga tushirish (Docker, VPS)

```bash
# 1) Bir marta akkauntga kirish (telefon raqam, kod, 2FA parol so'raladi)
docker compose run --rm tg_reply_me python login.py

# 2) Fonda doimiy ishga tushirish
docker compose up -d --build

# Loglar
docker compose logs -f
```

Sessiya `sessions/` papkasida saqlanadi — uni hech kimga bermang, u akkauntingizga to'liq kirish beradi.

## Docker'siz

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python login.py
python main.py
```

## Tekshirish

- Botga `/start` yozing — "Ishlayapman ✅" javobi kelishi kerak.
- Boshqa akkauntdan guruhda `@sizning_username` yozing yoki xabaringizga reply qiling — botga xabarnoma keladi.
- Testlar: `pip install pytest && pytest`
