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

## Mac'da eng oson yo'l

1. Terminalda `python3 --version` yozing. Python yo'q bo'lsa, macOS Command Line Tools'ni
   o'rnatishni taklif qiladi — **Install / Continue** bosing va tugashini kuting.
2. Loyiha papkasida:
   ```bash
   bash start.command
   ```
   Birinchi marta API_ID, API_HASH, BOT_TOKEN, keyin telefon raqam va kodni so'raydi.
   Keyingi safar shu buyruq botni darhol ishga tushiradi.

## Bepul serverda 24/7 (Oracle Cloud Free)

1. https://www.oracle.com/cloud/free/ da ro'yxatdan o'ting (karta faqat tekshirish uchun).
2. **Create a VM instance**: Image — **Ubuntu**, Shape — **VM.Standard.E2.1.Micro**
   (*Always Free-eligible*). *Add SSH keys* bo'limida **Save private key** ni bosing.
3. Mac Terminal'da serverga ulaning (`<IP>` — instansiya sahifasidagi *Public IP address*):
   ```bash
   chmod 600 ~/Downloads/ssh-key-*.key
   ssh -i ~/Downloads/ssh-key-*.key ubuntu@<IP>
   ```
4. Serverda bitta buyruq:
   ```bash
   bash <(curl -fsSL https://raw.githubusercontent.com/abdulazizcoder0901/tg_reply_me/claude/affectionate-cerf-k66w38/deploy/install.sh)
   ```
   API_ID, API_HASH, BOT_TOKEN, telefon raqam va kodni so'raydi, keyin bot `systemd` xizmati
   sifatida doimiy ishlaydi (server qayta yonsa ham o'zi ishga tushadi).

Loglar: `sudo journalctl -u tg_reply_me -f`. Kodni yangilash — 4-qadamdagi buyruqni qayta ishga tushiring.

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
