import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from django.contrib.auth.models import User
from complaints.models import Complaint, Verification, UserProfile
from rest_framework.test import APIClient
from rest_framework import status

def run_test():
    print("🚀 Starting Deletion Logic Verification...")

    # 1. Setup Users
    reporter_username = "deleter_test"
    upvoter_username = "upvoter_test"
    password = "password123$"

    # Clean up previous run
    User.objects.filter(username__in=[reporter_username, upvoter_username]).delete()

    reporter = User.objects.create_user(username=reporter_username, password=password)
    upvoter = User.objects.create_user(username=upvoter_username, password=password)
    
    print("✅ Users created.")

    # 2. Create Complaint (as Reporter)
    client = APIClient()
    client.force_authenticate(user=reporter)
    
    complaint_data = {
        "title": "To be deleted",
        "description": "This is a mistake",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "category": "OTHERS"
    }
    
    response = client.post('/api/complaints/', complaint_data)
    if response.status_code != 201:
        print(f"❌ Failed to create complaint: {response.data}")
        return
    
    complaint_id = response.data['id']
    print(f"✅ Complaint created (ID: {complaint_id})")

    # 3. Verify Complaint (as Upvoter) - To test point revocation
    client.force_authenticate(user=upvoter)
    response = client.post(f'/api/complaints/{complaint_id}/verify/')
    
    if response.status_code != 200:
        print(f"❌ Failed to verify complaint: {response.data}")
        return
        
    # Check Upvoter Points (Should be 10)
    upvoter.refresh_from_db()
    print(f"✅ Upvoter verified. Points: {upvoter.profile.points} (Expected: 10)")
    if upvoter.profile.points != 10:
        print("❌ Points logic failed (Verification).")
        return

    # 4. Delete Complaint (as Reporter)
    client.force_authenticate(user=reporter)
    response = client.delete(f'/api/complaints/{complaint_id}/')
    
    if response.status_code == 204:
        print("✅ Complaint deleted successfully.")
    else:
        print(f"❌ Failed to delete complaint: {response.status_code} - {response.data}")
        return

    # 5. Verify Deletion
    if Complaint.objects.filter(id=complaint_id).exists():
        print("❌ Complaint still exists in DB!")
        return
    else:
        print("✅ Complaint removed from DB.")

    # 6. Verify Point Revocation
    # When complaint is deleted, the Verification object is cascade deleted.
    # The post_delete signal on Verification should revoke the points.
    upvoter.refresh_from_db()
    print(f"🔍 Checking Upvoter Points after deletion: {upvoter.profile.points}")
    
    if upvoter.profile.points == 0:
        print("✅ Points revoked successfully! (Expected: 0)")
    else:
        print(f"❌ Points NOT revoked. Current: {upvoter.profile.points}")

if __name__ == "__main__":
    run_test()
