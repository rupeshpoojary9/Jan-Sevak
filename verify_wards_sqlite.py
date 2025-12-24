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
            'django.contrib.contenttypes',
            'complaints',
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

from complaints.models import Ward

count = Ward.objects.count()
print(f"Total Wards in SQLite: {count}")

if count < 24:
    print("⚠️  Wards seem missing. Expected ~24.")
    # List existing
    print("Existing Wards:", [w.name for w in Ward.objects.all()])
else:
    print("✅ Wards look complete.")
