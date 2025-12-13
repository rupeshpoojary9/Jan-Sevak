import os
import django
import time

# Setup Django Environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jan_sevak.settings")
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

def verify_ai():
    print("Setting up test user...")
    user, created = User.objects.get_or_create(username="ai_tester")
    if created:
        user.set_password("password123")
        user.save()

    client = APIClient()
    client.force_authenticate(user=user)
    print("Authenticated as ai_tester.")

    # Prepare Image
    image_path = "/Users/rupeshpoojary/.gemini/antigravity/brain/85fe3332-a40c-4da5-9188-c6c165202bdc/test_pothole_1764858543637.png"
    if not os.path.exists(image_path):
        print(f"Image not found at {image_path}")
        return

    with open(image_path, 'rb') as img:
        image_data = SimpleUploadedFile(
            name='test_pothole.png',
            content=img.read(),
            content_type='image/png'
        )

        data = {
            'title': 'AI Verification Pothole',
            'description': 'Large pothole test for AI verification.',
            'category': 'POTHOLE',
            'latitude': 19.01,
            'longitude': 72.85,
            'location_address': 'Test Location',
            'image': image_data
        }

        print("Submitting complaint via APIClient...")
        response = client.post('/api/complaints/', data, format='multipart')

        if response.status_code != 201:
            print(f"Submission failed: {response.status_code}")
            print(response.data)
            return

        complaint_id = response.data['id']
        print(f"Complaint submitted with ID: {complaint_id}")

        # Poll for results
        print("Polling for AI analysis...")
        for i in range(15):
            time.sleep(2)
            res = client.get(f'/api/complaints/{complaint_id}/')
            data = res.data
            score = data.get('urgency_score', 0)
            verified = data.get('ai_verified_category', False)
            
            print(f"Attempt {i+1}: Urgency Score = {score}, Verified = {verified}")
            
            if score > 0:
                print("\nSUCCESS: AI Analysis Complete!")
                print(f"Final Urgency Score: {score}")
                print(f"Category Verified: {verified}")
                return
        
        print("\nTIMEOUT: AI analysis took too long.")

if __name__ == "__main__":
    verify_ai()
