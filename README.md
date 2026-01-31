# 🎓 AI Taqdimot va Referat Bot

Ushbu loyiha Telegram orqali **referat, mustaqil ish va taqdimot (slide)**larni avtomatik tayyorlab beruvchi AI bot hisoblanadi.  
Bot Django backend va OpenAI API yordamida ishlaydi hamda foydalanuvchi balansiga asoslangan pullik tizimga ega.

---

## 🚀 Asosiy imkoniyatlar

- 📄 Referat va Mustaqil ish avtomatik yaratish
- 📊 Taqdimot (slide) kontentini tayyorlash
- 🤖 AI yordamida akademik uslub
- 💰 Balans va to‘lov tizimi
- 🧾 Har bir ish uchun avtomatik balansdan yechish
- 📂 Word (.docx) formatda fayl berish
- 👤 Telegram user bilan bog‘langan hisob

---

## 🛠 Texnologiyalar

- **Python 3.10+**
- **Django / Django REST Framework**
- **Telegram Bot API (pyTelegramBotAPI)**
- **OpenAI API**
- **PostgreSQL**
- **python-docx**
- **Requests**

---

## 📁 Loyiha strukturasi

Taqdimotbot/
├── bot.py
├── handlers/
│ ├── referat.py
│ ├── taqdimot.py
│ └── balance.py
├── taqdimot_app/
│ ├── models.py
│ ├── api/
│ │ └── views.py
│ ├── services/
│ │ ├── ai_services.py
│ │ ├── balance_service.py
│ │ ├── prompt_builder.py
│ │ └── word_services.py
├── keyboards/
├── utils/
├── media/
├── manage.py
└── requirements.txt


---

## ⚙️ O‘rnatish (Installation)

### 1️⃣ Repozitoriyani yuklab olish

```bash
git clone https://github.com/username/taqdimotbot.git
cd taqdimotbot
2️⃣ Virtual environment yaratish
python3 -m venv .venv
source .venv/bin/activate
3️⃣ Kerakli kutubxonalarni o‘rnatish
pip install -r requirements.txt
4️⃣ .env fayl yaratish
SECRET_KEY=django-secret-key
DEBUG=True

OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

DATABASE_NAME=taqdimot_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
5️⃣ Migratsiyalarni bajarish
python manage.py makemigrations
python manage.py migrate
6️⃣ Django serverni ishga tushirish
python manage.py runserver
7️⃣ Telegram botni ishga tushirish
python bot.py
💳 To‘lov va balans logikasi
Har bir referat yoki mustaqil ish narxi: 4000 so‘m

Foydalanuvchi balansida yetarli mablag‘ bo‘lsa:

Ish tayyorlanadi

Balansdan avtomatik 4000 so‘m yechiladi

Mablag‘ yetarli bo‘lmasa:

Hisobingizda mablag‘ yetarli emas.
Balansingiz: 1000 so‘m
Kerakli summa: 4000 so‘m
📊 Balans formulasi
BALANS = jami to‘lovlar − jami ishlatilgan summa
🧠 AI ishlash prinsipi
Prompt prompt_builder.py orqali yaratiladi

OpenAI’dan faqat JSON format qabul qilinadi

JSON asosida Word fayl avtomatik yaratiladi

Texnik xatolik bo‘lsa — default akademik struktura ishlatiladi