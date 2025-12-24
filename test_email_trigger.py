import os
import django
from django.conf import settings
from django.contrib.auth.models import User
from complaints.models import Complaint, Ward, Verification
from unittest.mock import patch

# 1. Create Users
print("Creating users...")
reporter, _ = User.objects.get_or_create(username='test_reporter', email='reporter@example.com')
verifier, _ = User.objects.get_or_create(username='test_verifier', email='verifier@example.com')

# 2. Create Ward
print("Creating ward...")
ward, _ = Ward.objects.get_or_create(name='TestWard', full_name='Test Ward for Email', officer_email='officer@example.com')

# 3. Create Complaint
print("Creating complaint...")
complaint = Complaint.objects.create(
    title="Test Email Trigger",
    description="Testing if email sends on verification",
    category="POTHOLE",
    ward=ward,
    reporter=reporter,
    location_address="Test Loc",
    latitude=19.0,
    longitude=72.0
)

# Ensure no verifications yet
complaint.verifications.all().delete()

# 4. Verify - Should trigger email
print("Verifying complaint (simulating community vote)...")

# We patch send_mail to intercept the call
with patch('django.core.mail.send_mail') as mocked_send_mail:
    # Create verification
    Verification.objects.create(user=verifier, complaint=complaint)
    
    if mocked_send_mail.called:
        print("\n✅ SUCCESS: send_mail was triggered!")
        args, kwargs = mocked_send_mail.call_args
        subject = args[0]
        recipients = args[3]
        print(f"Subject: {subject}")
        print(f"Recipients: {recipients}")
        
        expected_email = os.getenv('EMAIL_OVERRIDE_ADDRESS')
        if expected_email and expected_email in recipients:
             print(f"✅ SUCCESS: Recipient matches EMAIL_OVERRIDE_ADDRESS ({expected_email}).")
        else:
             print(f"⚠️ WARNING: Recipient is {recipients}, expected {expected_email}.")
    else:
        print("\n❌ FAILURE: send_mail was NOT triggered.")

# Cleanup
print("\nCleaning up...")
complaint.delete()
