import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.models import Complaint, Verification, Ward
from django.contrib.auth import get_user_model

User = get_user_model()

def test_smart_threshold():
    # Setup
    user, _ = User.objects.get_or_create(username="threshold_tester", email="tester@example.com")
    ward, _ = Ward.objects.get_or_create(name="T-Ward", defaults={"full_name": "Test Ward", "officer_email": "officer@example.com"})
    
    # Test 1: High Urgency (Score 9)
    print("\n--- Test 1: High Urgency (Score 9) ---")
    c1 = Complaint.objects.create(
        title="High Urgency Test", description="Desc", category="POTHOLE", 
        ward=ward, latitude=0, longitude=0, urgency_score=9, reporter=user
    )
    print(f"Created Complaint {c1.id} with Urgency 9")
    
    # Verify once
    print("Adding 1st Verification...")
    Verification.objects.create(complaint=c1, user=user)
    # Expected: Email sent (Check logs manually for "Email sent to...")

    # Test 2: Low Urgency (Score 5)
    print("\n--- Test 2: Low Urgency (Score 5) ---")
    c2 = Complaint.objects.create(
        title="Low Urgency Test", description="Desc", category="GARBAGE", 
        ward=ward, latitude=0, longitude=0, urgency_score=5, reporter=user
    )
    print(f"Created Complaint {c2.id} with Urgency 5")
    
    # Verify 1
    print("Adding 1st Verification...")
    Verification.objects.create(complaint=c2, user=user)
    
    # Verify 2 (Need different user)
    user2, _ = User.objects.get_or_create(username="voter2")
    print("Adding 2nd Verification...")
    Verification.objects.create(complaint=c2, user=user2)
    
    # Verify 3 (Need different user)
    user3, _ = User.objects.get_or_create(username="voter3")
    print("Adding 3rd Verification...")
    Verification.objects.create(complaint=c2, user=user3)
    # Expected: Email sent ONLY after 3rd verification

if __name__ == "__main__":
    test_smart_threshold()
