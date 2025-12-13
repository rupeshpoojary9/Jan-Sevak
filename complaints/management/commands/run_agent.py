from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from complaints.models import Complaint, Ward
from complaints.agents.escalation_agent import run_escalation_agent
import os

class Command(BaseCommand):
    help = 'Runs the LangGraph Escalation Agent'

    def handle(self, *args, **options):
        self.stdout.write("🤖 Starting Escalation Agent Test...")
        
        # Ensure API Key is set for LangChain
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            self.stdout.write(f"🔑 API Key Configured: {api_key[:5]}...")
        else:
            self.stdout.write(self.style.ERROR("❌ GEMINI_API_KEY not found! Agent might fail."))

        # 1. Create Dummy Complaint
        ward, _ = Ward.objects.get_or_create(name="A", defaults={"full_name": "Colaba", "officer_email": "ac.a@mcgm.gov.in"})
        
        complaint = Complaint.objects.create(
            title="Agent Test Pothole",
            description="Testing LangGraph Agent via Command",
            category="POTHOLE",
            urgency_score=9,
            ward=ward,
            latitude=18.9,
            longitude=72.8,
            status=Complaint.Status.NEW
        )
        
        # Backdate
        complaint.created_at = timezone.now() - timedelta(days=2)
        complaint.save()
        
        self.stdout.write(f"✅ Created Test Complaint #{complaint.id}")
        
        # 2. Run Agent
        try:
            self.stdout.write("🚀 Invoking Agent...")
            result = run_escalation_agent(complaint.id)
            self.stdout.write(f"🏁 Agent Finished. Result: {result.get('final_status')}")
            
            # 3. Verify
            complaint.refresh_from_db()
            if complaint.status == Complaint.Status.ESCALATED and complaint.escalation_level == 1:
                self.stdout.write(self.style.SUCCESS("✅ SUCCESS: Complaint Escalated!"))
                self.stdout.write(f"📧 Drafted Email:\n{result.get('draft_email')[:200]}...")
            else:
                self.stdout.write(self.style.ERROR(f"❌ FAILURE: Status is {complaint.status}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Agent Error: {e}"))
