import os
import django
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

print(f"Testing Postgres Connection...")
print(f"Database Host: {settings.DATABASES['default']['HOST']}")
print(f"Database Port: {settings.DATABASES['default']['PORT']}")

try:
    conn = connections['default']
    c = conn.cursor()
    print("✅ Successfully connected to Postgres!")
except OperationalError as e:
    print(f"❌ Connection Failed: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
