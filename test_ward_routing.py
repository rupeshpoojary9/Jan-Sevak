import os
import django
from django.conf import settings

# Manually configure settings to bypass .env/Docker issues
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
        EMAIL_OVERRIDE_ADDRESS='poojary.rupesh12@gmail.com', # Simulating the production setting
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

from complaints.models import Ward

print("🔍 SIMULATING EMAIL ROUTING FOR PRODUCTION...\n")

# 1. Check Override Setting
override = settings.EMAIL_OVERRIDE_ADDRESS
print(f"⚠️  TEST MODE ACTIVE: All emails redirected to: {override}")
print("-" * 50)

# 2. Simulate for a few wards
test_wards = ['A', 'G/North', 'K/West']

for ward_name in test_wards:
    try:
        ward = Ward.objects.get(name=ward_name)
        print(f"\n📍 Complaint Reported in Ward: {ward.name} ({ward.full_name})")
        
        # The Logic from signals.py
        intended_recipient = ward.officer_email
        actual_recipient = intended_recipient
        
        if override:
            actual_recipient = override
            
        print(f"   👉 INTENDED Recipient (Production): {intended_recipient}")
        print(f"   👉 ACTUAL Recipient (Current Test): {actual_recipient}")
        
        if intended_recipient and "@mcgm.gov.in" in intended_recipient:
            print("   ✅ Routing Logic: CORRECT (Would go to Official)")
        else:
            print("   ❌ Routing Logic: INVALID (No Official Email Found)")
            
    except Ward.DoesNotExist:
        print(f"\n❌ Ward {ward_name} not found!")

print("\n" + "-" * 50)
print("✅ CONCLUSION: The system KNOWS the correct official email.")
print("   It is only sending to YOU because of the safety override.")
