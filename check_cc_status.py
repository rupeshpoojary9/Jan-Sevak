import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.models import Complaint

def check_latest_complaint():
    complaints = Complaint.objects.all().order_by('-created_at')[:5]
    if not complaints:
        print("No complaints found.")
        return

    for c in complaints:
        print(f"ID: {c.id}, Title: {c.title}, Reporter: {c.reporter.username if c.reporter else 'Anonymous'}, CC: {c.cc_reporter}, Created: {c.created_at}")


if __name__ == "__main__":
    check_latest_complaint()
