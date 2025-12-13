import pytest
from unittest.mock import patch, MagicMock
from complaints.agents.escalation_agent import run_escalation_agent, check_status, draft_notice, send_email, update_db, AgentState
from complaints.models import Complaint, Ward
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestEscalationAgent:
    @pytest.fixture
    def ward(self):
        return Ward.objects.create(name="A", full_name="Colaba", officer_email="ac.a@mcgm.gov.in")

    @pytest.fixture
    def complaint(self, ward):
        c = Complaint.objects.create(
            title="Agent Test",
            description="Fix me",
            category="POTHOLE",
            ward=ward,
            latitude=18.9,
            longitude=72.8,
            urgency_score=9,
            status=Complaint.Status.NEW
        )
        c.created_at = timezone.now() - timedelta(hours=25) # Old enough
        c.save()
        return c

    def test_check_status_needs_escalation(self, complaint):
        """Test that check_status correctly identifies high urgency old complaints."""
        state = {"complaint_id": complaint.id}
        result = check_status(state)
        assert result["status"] == "NEEDS_ESCALATION"
        assert result["urgency"] == 9

    def test_check_status_no_action(self, complaint):
        """Test that check_status ignores low urgency complaints."""
        complaint.urgency_score = 5
        complaint.save()
        state = {"complaint_id": complaint.id}
        result = check_status(state)
        assert result["final_status"] == "NO_ACTION_NEEDED"

    @patch("complaints.agents.escalation_agent.ChatGoogleGenerativeAI")
    def test_draft_notice(self, MockLLMClass, complaint):
        """Test that draft_notice calls the LLM."""
        # Setup Mock
        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Drafted Legal Notice"
        mock_llm_instance.invoke.return_value = mock_response
        MockLLMClass.return_value = mock_llm_instance
        
        state = {"complaint_id": complaint.id}
        result = draft_notice(state)
        
        assert result["draft_email"] == "Drafted Legal Notice"
        MockLLMClass.assert_called_once()
        mock_llm_instance.invoke.assert_called_once()

    @patch("complaints.agents.escalation_agent.send_mail")
    def test_send_email(self, mock_send_mail, complaint):
        """Test that send_email calls Django's send_mail."""
        state = {"complaint_id": complaint.id, "draft_email": "Body"}
        result = send_email(state)
        mock_send_mail.assert_called_once()
        assert "recipient" in result

    def test_update_db(self, complaint):
        """Test that update_db changes status to ESCALATED."""
        state = {"complaint_id": complaint.id}
        result = update_db(state)
        
        complaint.refresh_from_db()
        assert complaint.status == Complaint.Status.ESCALATED
        assert complaint.escalation_level == 1
        assert result["final_status"] == "ESCALATED"
