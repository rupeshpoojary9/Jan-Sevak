import os
import django
from django.conf import settings
from django.contrib.auth.models import User
from complaints.models import Complaint, Ward, Verification
import time

# 1. Create Users
print("Creating users...")
# Use unique names to avoid conflicts if run multiple times
timestamp = int(time.time())
reporter, _ = User.objects.get_or_create(username=f'real_reporter_{timestamp}', email='reporter@example.com')
verifier, _ = User.objects.get_or_create(username=f'real_verifier_{timestamp}', email='verifier@example.com')

# 2. Create Ward
print("Creating ward...")
ward, _ = Ward.objects.get_or_create(name='TestWard', defaults={'full_name': 'Test Ward for Email', 'officer_email': 'officer@example.com'})

# 3. Create Complaint
print("Creating complaint...")
complaint = Complaint.objects.create(
    title=f"Real Email Test {timestamp}",
    description="Testing actual SMTP sending",
    category="POTHOLE",
    ward=ward,
    reporter=reporter,
    location_address="Test Loc",
    latitude=19.0,
    longitude=72.0
)

# 4. Verify - Should trigger REAL email
print("Verifying complaint (simulating community vote)...")
print(f"Expecting email to be sent to override address: {os.getenv('EMAIL_OVERRIDE_ADDRESS')}")

# This will trigger the signal, which calls send_mail
# BUT signals use the default connection. To debug, we need to manually send an email to see the output.
# The signal will still fail silently or print error, but let's try to send a direct email first to debug the connection.

print("Attempting DIRECT email send with debug...")
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage

try:
    connection = get_connection()
    connection.open() # This connects to the server
    
    # Enable debug on the underlying SMTP object
    if connection.connection:
        connection.connection.set_debuglevel(1)
        
    email = EmailMessage(
        'Debug Test',
        'Body',
        settings.EMAIL_HOST_USER,
        [os.getenv('EMAIL_OVERRIDE_ADDRESS')],
        connection=connection
    )
    email.send()
    print("✅ Direct email sent successfully!")
    connection.close()
    
    # Now try the signal
    print("\nNow triggering signal...")
    Verification.objects.create(user=verifier, complaint=complaint)
    print("Verification created.")

except Exception as e:
    print(f"❌ Direct email failed: {e}")

# Cleanup
print("Cleaning up...")
complaint.delete()
reporter.delete()
verifier.delete()
