from complaints.models import Complaint, Ward
from django.contrib.auth.models import User
from django.conf import settings
import datetime

# Ensure we use console backend to see output
# settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print("\n" + "="*50)
print("SIMULATING COMPLAINT CREATION & EMAIL NOTIFICATION")
print("="*50 + "\n")

# Create dummy data
user, _ = User.objects.get_or_create(username='test_citizen')
ward, _ = Ward.objects.get_or_create(name='D-Test', full_name='Debug Ward', officer_email='officer@debug.com')

# Create Complaint
# This triggers the post_save signal in complaints/signals.py
complaint = Complaint.objects.create(
    title="Overflowing Garbage Bin",
    description="The garbage bin at the corner of MG Road is overflowing and causing a bad smell. Please address immediately.",
    category="GARBAGE",
    ward=ward,
    latitude=19.0760,
    longitude=72.8777,
    reporter=user,
    urgency_score=8, # High urgency to trigger "URGENT" subject
    location_address="Corner of MG Road, Near Central Park, Mumbai"
)

print("\n" + "="*50)
print("SIMULATION COMPLETE")
print("="*50 + "\n")
