import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from complaints.models import Complaint, Ward, Verification
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.mark.django_db
class TestComplaintViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="password123")

    @pytest.fixture
    def ward(self):
        return Ward.objects.create(name="A", full_name="Colaba", officer_email="ac.a@mcgm.gov.in")

    @pytest.fixture
    def complaint(self, user, ward):
        return Complaint.objects.create(
            title="Test Pothole",
            description="Fix this",
            category="POTHOLE",
            ward=ward,
            latitude=18.9,
            longitude=72.8,
            reporter=user,
            status=Complaint.Status.NEW
        )

    def test_list_complaints(self, api_client, complaint):
        """Test listing complaints."""
        response = api_client.get('/api/complaints/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Test Pothole"

    @pytest.mark.django_db
    def test_create_complaint_authenticated(self, api_client, user, ward):
        """Test creating a complaint as a logged-in user."""
        api_client.force_authenticate(user=user)
        
        # Create a dummy image (Valid 1x1 GIF)
        valid_image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04'
            b'\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44'
            b'\x01\x00\x3b'
        )
        image = SimpleUploadedFile("test.gif", valid_image_content, content_type="image/gif")
        
        data = {
            "title": "New Issue",
            "description": "Garbage pile",
            "category": "GARBAGE",
            "latitude": 19.0,
            "longitude": 72.9,
            "location_address": "Test Loc",
            "ward": ward.id, # Add Ward ID
            "image": image
        }
        
        # Mock AI Service to bypass API call
        from unittest.mock import patch
        with patch('complaints.ai_service.analyze_complaint') as mock_ai:
            # Return: is_valid, reason, score, verified
            mock_ai.return_value = (True, None, 8, True)
            
            response = api_client.post('/api/complaints/', data, format='multipart')
            
            if response.status_code != status.HTTP_201_CREATED:
                with open("test_debug.log", "a") as f:
                    f.write(f"Create Failed: {response.data}\n")
            
            assert response.status_code == status.HTTP_201_CREATED
            assert Complaint.objects.count() == 1
            assert Complaint.objects.first().ward is not None

    def test_create_complaint_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot create complaints."""
        data = {"title": "Fail"}
        response = api_client.post('/api/complaints/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_upvote_complaint(self, api_client, user, complaint):
        """Test upvoting a complaint."""
        api_client.force_authenticate(user=user)
        
        # First Upvote
        response = api_client.post(f'/api/complaints/{complaint.id}/verify/') # Fix URL
        if response.status_code != 200:
             with open("test_debug.log", "a") as f:
                f.write(f"Upvote Part 1 Failed: {response.data}\n")
        
        assert response.status_code == status.HTTP_200_OK
        complaint.refresh_from_db()
        with open("test_debug.log", "a") as f:
            f.write(f"Verification Count Part 1: {complaint.verifications.count()}\n")
        assert complaint.verifications.count() == 1
        
        # Duplicate Upvote (Should fail or return 200 but not increment)
        # Based on implementation, it might toggle or error. Let's assume it prevents duplicate.
        response = api_client.post(f'/api/complaints/{complaint.id}/verify/') # Fix URL
        if response.status_code != 400:
             with open("test_debug.log", "a") as f:
                f.write(f"Upvote Part 2 Failed (Expected 400): {response.status_code} {response.data}\n")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        complaint.refresh_from_db()
        with open("test_debug.log", "a") as f:
            f.write(f"Verification Count Part 2: {complaint.verifications.count()}\n")
        assert complaint.verifications.count() == 1
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        complaint.refresh_from_db()
        assert complaint.verifications.count() == 1

    def test_delete_complaint_owner(self, api_client, user, complaint):
        """Test that the owner can delete a NEW complaint."""
        api_client.force_authenticate(user=user)
        response = api_client.delete(f'/api/complaints/{complaint.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Complaint.objects.count() == 0

    def test_delete_complaint_not_owner(self, api_client, complaint):
        """Test that another user cannot delete the complaint."""
        other_user = User.objects.create_user(username="other", password="123")
        api_client.force_authenticate(user=other_user)
        
        response = api_client.delete(f'/api/complaints/{complaint.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_complaint_processed(self, api_client, user, complaint):
        """Test that processed complaints (e.g., VERIFIED) cannot be deleted."""
        complaint.status = Complaint.Status.VERIFIED
        complaint.save()
        
        api_client.force_authenticate(user=user)
        response = api_client.delete(f'/api/complaints/{complaint.id}/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST # Or 403 depending on implementation
        assert Complaint.objects.count() == 1
