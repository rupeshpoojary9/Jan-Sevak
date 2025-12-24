import os
import django
from django.conf import settings
from django.contrib.auth.models import User
from complaints.models import Complaint, Ward, Verification
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

def run_test():
    print("🚀 Starting Real Workflow Test (User Acceptance)...")
    
    # 1. Setup Data
    print("\n[1/3] Setting up test data...")
    # Use unique names
    timestamp = int(time.time())
    reporter, _ = User.objects.get_or_create(username=f'uat_reporter_{timestamp}', email='poojary.rupesh12@gmail.com')
    verifier, _ = User.objects.get_or_create(username=f'uat_verifier_{timestamp}', email='verifier@test.com')
    ward, _ = Ward.objects.get_or_create(name='UAT', defaults={'full_name': 'UAT Ward', 'officer_email': 'officer@test.com'})
    
    # 2. Create Complaint
    print("\n[2/3] Creating UAT Complaint...")
    complaint = Complaint.objects.create(
        title=f"UAT Magic Link Test {timestamp}",
        description="Please click the link in the email to resolve this.",
        category="POTHOLE",
        ward=ward,
        reporter=reporter,
        location_address="UAT Location",
        latitude=19.0,
        longitude=72.0
    )
    print(f"✅ Complaint #{complaint.id} created.")

    # 3. Verify Complaint & Trigger Real Email
    print("\n[3/3] Triggering Real Email...")
    print(f"   Target: {os.getenv('EMAIL_OVERRIDE_ADDRESS')}")
    
    try:
        Verification.objects.create(user=verifier, complaint=complaint)
        print("✅ Verification created. Email should be sent now.")
        print("👉 Please check your inbox for 'Formal Grievance' and click the link!")
    except Exception as e:
        print(f"❌ Error triggering email: {e}")

run_test()
