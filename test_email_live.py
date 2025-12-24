import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

print(f"Testing email configuration...")
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"Override Address: {settings.EMAIL_OVERRIDE_ADDRESS}")

try:
    print("Attempting to send email...")
    send_mail(
        'Jan Sevak Live Email Test',
        'This is a test email to verify the SMTP configuration is live and working. If you received this, the system is ready.',
        settings.DEFAULT_FROM_EMAIL,
        ['test_recipient@example.com'], # This should be redirected to override address
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Email failed to send: {e}")
