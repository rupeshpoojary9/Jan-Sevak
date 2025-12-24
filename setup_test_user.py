import os
import django
from django.conf import settings

# Manually configure settings to force SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        SECRET_KEY='test_key',
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'complaints',
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

from django.contrib.auth.models import User

username = 'rupesh1'
email = 'rupesh1@example.com'
password = 'password123$'

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username, email, password)
    print(f"✅ User '{username}' created successfully.")
else:
    print(f"ℹ️ User '{username}' already exists.")
