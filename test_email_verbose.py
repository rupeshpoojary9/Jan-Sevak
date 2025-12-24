import os
import django
from django.core.mail import send_mail, get_connection
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

print(f"Testing email configuration with VERBOSE logging...")
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"Override Address: {settings.EMAIL_OVERRIDE_ADDRESS}")

try:
    # Get connection and enable debug logging
    connection = get_connection()
    # connection.set_debuglevel(1) # This prints to stdout/stderr

    print("Attempting to send email...")
    send_mail(
        'Jan Sevak Verbose Test',
        'This is a verbose test email. Please check headers.',
        settings.DEFAULT_FROM_EMAIL,
        ['test_recipient@example.com'], 
        fail_silently=False,
        connection=connection
    )
    print("✅ Email sent successfully (according to Django)!")
except Exception as e:
    print(f"❌ Email failed to send: {e}")
