import os
import django

# Use default settings (which now point to Postgres via .env)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from django.contrib.auth.models import User

username = 'rupesh1'
email = 'rupesh1@example.com'
password = 'password123$'

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username, email, password)
    print(f"✅ Postgres: User '{username}' created successfully.")
else:
    print(f"ℹ️ Postgres: User '{username}' already exists.")
