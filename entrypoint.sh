#!/bin/sh
set -e

# Faqat web uchun migration va server
# Bot uchun bu script ishlamaydi (command: python bot.py)

echo "⏳ Running migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 Checking superuser..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email    = os.getenv("DJANGO_SUPERUSER_EMAIL",    "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser yaratildi: {username}")
else:
    print(f"ℹ️  Superuser allaqachon bor: {username}")
EOF

echo "🚀 Starting server..."
exec "$@"