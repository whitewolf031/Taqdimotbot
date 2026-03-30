#!/bin/sh
set -e

echo "⏳ Bot container ishga tushmoqda..."

# Agar kerak bo‘lsa Django migrations va collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# ✅ Botni ishga tushirish
exec python bot.py