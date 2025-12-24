import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

# Use the override address (the user's email) as the recipient
recipient = settings.EMAIL_OVERRIDE_ADDRESS or 'poojary.rupesh12@gmail.com'

print(f"Testing REAL delivery to: {recipient}")

try:
    send_mail(
        'Jan Sevak FINAL Verification',
        f'This email confirms that your SMTP settings are correct and you can receive emails.\n\nIgnore the previous error about "test_recipient@example.com" - that happened because "example.com" is a fake domain.\n\nThis email proves the system works.',
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
    print(f"✅ Email sent to {recipient}!")
except Exception as e:
    print(f"❌ Email failed: {e}")
