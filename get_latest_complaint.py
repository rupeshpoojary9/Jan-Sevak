import os
import django
from django.conf import settings

# Use default settings (Postgres via .env)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.models import Complaint
from django.contrib.auth.models import User

try:
    # Debug: List all complaints
    print(f"Total Complaints: {Complaint.objects.count()}")
    
    # Check for the specific gibberish complaint
    gibberish = Complaint.objects.filter(description__icontains="fefgsefsgsdgs")
    if gibberish.exists():
        print(f"⚠️ Found {gibberish.count()} gibberish complaints:")
        for c in gibberish:
             print(f"ID: {c.id}, Title: {c.title}, Reporter: {c.reporter.username if c.reporter else 'None'}, Status: {c.status}")
    else:
        print("✅ No gibberish complaints found in DB.")

    for c in Complaint.objects.all().order_by('-created_at')[:10]:
        print(f"ID: {c.id}, Title: {c.title}, Reporter: {c.reporter.username if c.reporter else 'None'}, Created: {c.created_at}")

    try:
        user = User.objects.get(username='rupesh1')
        # Get second latest complaint (Index 1) for debugging
        complaints = Complaint.objects.filter(reporter=user).order_by('-created_at')
        if complaints.count() >= 2:
            complaint = complaints[1]
            print(f"🔍 Debugging Second Latest Complaint (Total: {complaints.count()})")
        else:
            complaint = complaints.first()
            print("⚠️ Only one complaint found, showing latest.")
    except User.DoesNotExist:
        print("❌ User rupesh1 not found")
        complaint = None

    if complaint:
        print(f"✅ Found Complaint #{complaint.id}")
        print(f"Title: {complaint.title}")
        print(f"Status: {complaint.status}")
        print(f"Urgency Score: {complaint.urgency_score}")
        print(f"AI Verified Category: {complaint.ai_verified_category}")
        print(f"Description: {complaint.description}")
        print(f"Admin Token: {complaint.admin_token}")
        print(f"Magic Link: http://localhost:8000/api/resolve/{complaint.id}/{complaint.admin_token}/")
    else:
        print("❌ No complaints found for rupesh1")

except User.DoesNotExist:
    print("❌ User rupesh1 not found")
