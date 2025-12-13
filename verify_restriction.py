import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.serializers import ComplaintSerializer
from complaints.models import Ward
from django.contrib.auth.models import User

def test_mumbai_restriction():
    print("\n" + "="*50)
    print("VERIFYING MUMBAI RESTRICTION")
    print("="*50 + "\n")

    # Create dummy user and ward if needed
    user, _ = User.objects.get_or_create(username='test_citizen')
    ward, _ = Ward.objects.get_or_create(name='D-Test', full_name='Debug Ward')

    # Test Case 1: Valid Mumbai Location
    valid_data = {
        'title': 'Valid Complaint',
        'description': 'This is in Mumbai',
        'category': 'POTHOLE',
        'ward': ward.id,
        'latitude': 19.0760,
        'longitude': 72.8777,
        'location_address': 'Mumbai',
        'reporter': user.id
    }
    
    serializer = ComplaintSerializer(data=valid_data)
    if serializer.is_valid():
        print("✅ Test Case 1 (Valid Mumbai Location): PASSED")
    else:
        print(f"❌ Test Case 1 (Valid Mumbai Location): FAILED - {serializer.errors}")

    # Test Case 2: Invalid Location (Delhi)
    invalid_data = {
        'title': 'Invalid Complaint',
        'description': 'This is in Delhi',
        'category': 'POTHOLE',
        'ward': ward.id,
        'latitude': 28.7041,
        'longitude': 77.1025,
        'location_address': 'Delhi',
        'reporter': user.id
    }

    serializer = ComplaintSerializer(data=invalid_data)
    if not serializer.is_valid():
        if 'location' in serializer.errors:
            print("✅ Test Case 2 (Invalid Location): PASSED - Correctly rejected")
            print(f"   Error Message: {serializer.errors['location'][0]}")
        else:
            print(f"❌ Test Case 2 (Invalid Location): FAILED - Rejected but wrong error: {serializer.errors}")
    else:
        print("❌ Test Case 2 (Invalid Location): FAILED - Accepted invalid location")

if __name__ == "__main__":
    test_mumbai_restriction()
