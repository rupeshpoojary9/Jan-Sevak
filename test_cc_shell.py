import os
import django
from django.conf import settings
from django.core import mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.models import Complaint
from django.contrib.auth import get_user_model

User = get_user_model()

def test_cc_logic():
    # Create or get user
    user, created = User.objects.get_or_create(username="rupesh_shell_test", email="imrupesh24@gmail.com")
    if created:
        user.set_password("Password@123")
        user.save()
        print(f"Created user {user.username}")
    else:
        print(f"Using existing user {user.username}")

    # Create complaint
    print("Creating complaint with cc_reporter=True...")
    from complaints.models import Ward
    ward = Ward.objects.first()
    if not ward:
        print("No Ward found. Creating one.")
        ward = Ward.objects.create(name="Test Ward", number="1", officer_email="officer@example.com")
    else:
        # Ensure officer_email is set
        if not ward.officer_email:
            ward.officer_email = "officer@example.com"
            ward.save()

    complaint = Complaint.objects.create(
        title="Shell Test for CC Feature",
        description="Testing if CC email is sent via Shell submission.",
        category="OTHERS",
        ward=ward,
        location_address="Test Location",
        latitude=19.0178,
        longitude=72.8478,
        is_anonymous=False,
        reporter=user,
        cc_reporter=True
    )
    
    print(f"Complaint created: {complaint.id}")

    # Create Verification to trigger email
    from complaints.models import Verification
    print("Creating Verification to trigger email...")
    Verification.objects.create(complaint=complaint, user=user)

    
    # Check if email was sent (if using locmem backend or similar, we can check mail.outbox)
    # But since we are in a script, we might not capture it unless we mock or check logs.
    # However, the signal prints "Adding reporter ... to CC list" to stdout.
    # So we should see that in the output.

if __name__ == "__main__":
    test_cc_logic()
