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
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'complaints',
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

from complaints.models import Ward

print("🔍 Checking Wards in SQLite...")
count = Ward.objects.count()
print(f"Current Ward Count: {count}")

wards_data = [
    # City
    {"name": "A", "full_name": "Colaba / Churchgate", "officer_email": "wardA@mcgm.gov.in"},
    {"name": "B", "full_name": "Sandhurst Road", "officer_email": "wardB@mcgm.gov.in"},
    {"name": "C", "full_name": "Marine Lines", "officer_email": "wardC@mcgm.gov.in"},
    {"name": "D", "full_name": "Grant Road", "officer_email": "wardD@mcgm.gov.in"},
    {"name": "E", "full_name": "Byculla", "officer_email": "wardE@mcgm.gov.in"},
    
    # Western Suburbs
    {"name": "H/West", "full_name": "Bandra West", "officer_email": "wardHW@mcgm.gov.in"},
    {"name": "H/East", "full_name": "Bandra East", "officer_email": "wardHE@mcgm.gov.in"},
    {"name": "K/West", "full_name": "Andheri West", "officer_email": "wardKW@mcgm.gov.in"},
    {"name": "K/East", "full_name": "Andheri East", "officer_email": "wardKE@mcgm.gov.in"},
    {"name": "P/South", "full_name": "Goregaon", "officer_email": "wardPS@mcgm.gov.in"},
    {"name": "P/North", "full_name": "Malad", "officer_email": "wardPN@mcgm.gov.in"},
    {"name": "R/South", "full_name": "Kandivali", "officer_email": "wardRS@mcgm.gov.in"},
    {"name": "R/Central", "full_name": "Borivali", "officer_email": "wardRC@mcgm.gov.in"},
    {"name": "R/North", "full_name": "Dahisar", "officer_email": "wardRN@mcgm.gov.in"},

    # Eastern Suburbs
    {"name": "L", "full_name": "Kurla", "officer_email": "wardL@mcgm.gov.in"},
    {"name": "M/East", "full_name": "Govandi", "officer_email": "wardME@mcgm.gov.in"},
    {"name": "M/West", "full_name": "Chembur", "officer_email": "wardMW@mcgm.gov.in"},
    {"name": "N", "full_name": "Ghatkopar", "officer_email": "wardN@mcgm.gov.in"},
    {"name": "S", "full_name": "Bhandup", "officer_email": "wardS@mcgm.gov.in"},
    {"name": "T", "full_name": "Mulund", "officer_email": "wardT@mcgm.gov.in"},
    
    # Central
    {"name": "F/North", "full_name": "Matunga", "officer_email": "wardFN@mcgm.gov.in"},
    {"name": "F/South", "full_name": "Parel", "officer_email": "wardFS@mcgm.gov.in"},
    {"name": "G/North", "full_name": "Dadar / Dharavi", "officer_email": "wardGN@mcgm.gov.in"},
    {"name": "G/South", "full_name": "Worli", "officer_email": "wardGS@mcgm.gov.in"},
]

if count < len(wards_data):
    print(f"⚠️  Missing wards! Populating now...")
    for data in wards_data:
        obj, created = Ward.objects.get_or_create(name=data["name"], defaults=data)
        if created:
            print(f"   ✅ Created: {data['name']}")
        else:
            # Update email if changed
            if obj.officer_email != data['officer_email']:
                obj.officer_email = data['officer_email']
                obj.save()
                print(f"   🔄 Updated: {data['name']}")
    print("✅ Population Complete.")
else:
    print("✅ All Wards Present.")
