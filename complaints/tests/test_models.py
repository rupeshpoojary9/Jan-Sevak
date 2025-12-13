import pytest
from complaints.models import Complaint, Ward
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestComplaintModel:
    def test_create_complaint_defaults(self):
        """Test that a complaint is created with correct default values."""
        ward = Ward.objects.create(name="A", full_name="Colaba", officer_email="ac.a@mcgm.gov.in")
        complaint = Complaint.objects.create(
            title="Test Pothole",
            description="A big pothole",
            category="POTHOLE",
            ward=ward,
            latitude=18.9,
            longitude=72.8
        )
        
        assert complaint.status == Complaint.Status.NEW
        assert complaint.escalation_level == 0
        assert complaint.urgency_score == 0
        assert complaint.is_anonymous is False

    def test_urgency_score_validation(self):
        """Test that urgency score must be between 0 and 10."""
        ward = Ward.objects.create(name="B", full_name="Sandhurst Road", officer_email="ac.b@mcgm.gov.in")
        complaint = Complaint(
            title="Invalid Urgency",
            description="Testing validation",
            category="GARBAGE",
            ward=ward,
            latitude=19.0,
            longitude=72.9,
            urgency_score=11 # Invalid
        )
        
        # Note: Django model validation isn't automatic on save(), usually called in forms/serializers.
        # But we can call full_clean() to test it.
        with pytest.raises(ValidationError):
            complaint.full_clean()

    def test_str_representation(self):
        """Test the string representation of the model."""
        ward = Ward.objects.create(name="C", full_name="Marine Lines", officer_email="ac.c@mcgm.gov.in")
        complaint = Complaint.objects.create(
            title="Broken Streetlight",
            description="Dark street",
            category="STREET_LIGHT",
            ward=ward,
            latitude=18.95,
            longitude=72.82
        )
        assert str(complaint) == f"{complaint.category} in {complaint.ward} ({complaint.status})"
