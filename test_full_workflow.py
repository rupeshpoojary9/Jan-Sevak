import os
import django
from django.conf import settings
from django.contrib.auth.models import User
from complaints.models import Complaint, Ward, Verification
from django.test import RequestFactory
from complaints.views import resolve_complaint
import re
from unittest.mock import patch

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

def run_test():
    print("🚀 Starting End-to-End Workflow Test...")
    
    # 1. Setup Data
    print("\n[1/5] Setting up test data...")
    # Clean previous run
    User.objects.filter(username__in=['e2e_reporter', 'e2e_verifier']).delete()
    Ward.objects.filter(name='E2E').delete()
    
    reporter = User.objects.create_user(username='e2e_reporter', email='reporter@test.com', password='pass')
    verifier = User.objects.create_user(username='e2e_verifier', email='verifier@test.com', password='pass')
    ward = Ward.objects.create(name='E2E', full_name='End to End Ward', officer_email='officer@test.com')
    
    # 2. Create Complaint
    print("\n[2/5] Reporter creating complaint...")
    complaint = Complaint.objects.create(
        title="E2E Test Complaint",
        description="Testing the full flow",
        category="POTHOLE",
        ward=ward,
        reporter=reporter,
        location_address="Test Loc",
        latitude=19.0,
        longitude=72.0
    )
    print(f"✅ Complaint #{complaint.id} created. Status: {complaint.status}")

    # 3. Verify Complaint & Capture Email
    print("\n[3/5] Verifier upvoting (triggering email)...")
    
    # We patch send_mail to capture the content instead of sending it
    with patch('complaints.signals.send_mail') as mock_send_mail:
        Verification.objects.create(user=verifier, complaint=complaint)
        
        if mock_send_mail.called:
            print("✅ Email trigger successful!")
            args, kwargs = mock_send_mail.call_args
            subject = args[0]
            body = args[1]
            recipient = args[3]
            
            print(f"   Subject: {subject}")
            print(f"   Recipient: {recipient}")
            
            # Extract Magic Link using Regex
            # Link format: http://127.0.0.1:8000/api/resolve/{id}/{token}/
            match = re.search(r'(http://127.0.0.1:8000/api/resolve/[\d]+/[a-f0-9\-]+/)', body)
            if match:
                magic_link = match.group(1)
                print(f"✅ Magic Link Extracted: {magic_link}")
            else:
                print("❌ Failed to extract Magic Link from email body!")
                return
        else:
            print("❌ Email was NOT triggered!")
            return

    # 4. Simulate Official Clicking the Link
    print("\n[4/5] Simulating Official clicking the Magic Link...")
    
    # Parse the URL to get args for the view
    # /api/resolve/{pk}/{token}/
    parts = magic_link.split('/')
    pk = int(parts[-3])
    token = parts[-2]
    
    # Create a fake request
    factory = RequestFactory()
    request = factory.get(magic_link)
    
    # Call the view directly
    response = resolve_complaint(request, pk=pk, token=token)
    
    if response.status_code == 200:
        print("✅ Resolution View returned 200 OK")
    else:
        print(f"❌ Resolution View failed with {response.status_code}")
        return

    # 5. Verify Final Status
    print("\n[5/5] Verifying final status in Database...")
    complaint.refresh_from_db()
    if complaint.status == 'RESOLVED':
        print(f"✅ SUCCESS! Complaint status is now: {complaint.status}")
    else:
        print(f"❌ FAILURE! Complaint status is: {complaint.status}")

    # Cleanup
    print("\nCleaning up...")
    complaint.delete()
    ward.delete()
    reporter.delete()
    verifier.delete()

run_test()
