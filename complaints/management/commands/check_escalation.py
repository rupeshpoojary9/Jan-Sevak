from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from complaints.models import Complaint
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Checks for high urgency complaints that need escalation'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking for complaints to escalate...")
        
        # Criteria: Urgency >= 8, Status NOT Resolved, Created > 24 hours ago
        threshold_time = timezone.now() - timedelta(hours=24)
        
        # Find complaints that need escalation (Level 0 -> 1)
        complaints_to_escalate = Complaint.objects.filter(
            urgency_score__gte=8,
            status__in=[Complaint.Status.NEW, Complaint.Status.VERIFIED, Complaint.Status.ESCALATED],
            created_at__lte=threshold_time,
            escalation_level=0
        )
        
        count = 0
        for complaint in complaints_to_escalate:
            self.escalate_complaint(complaint)
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f"✅ Escalated {count} complaints."))

    def escalate_complaint(self, complaint):
        # 1. Update Level
        complaint.escalation_level = 1
        complaint.status = Complaint.Status.ESCALATED
        complaint.save()
        
        # 2. Send Email to Senior Official
        subject = f"[ESCALATION LEVEL 1] Unresolved High Urgency Complaint #{complaint.id}"
        message = f"""
        URGENT ESCALATION NOTICE
        To: Deputy Municipal Commissioner
        
        This complaint has exceeded the 24-hour resolution window for High Urgency issues.
        
        Complaint Details:
        ------------------
        ID: #{complaint.id}
        Title: {complaint.title}
        Ward: {complaint.ward.name}
        Urgency: {complaint.urgency_score}/10
        Time Elapsed: {(timezone.now() - complaint.created_at).days} days
        
        Please intervene immediately.
        
        Jan Sevak Automated Escalation System
        """
        
        try:
            # Determine Recipient (Real vs Test)
            if settings.EMAIL_OVERRIDE_ADDRESS:
                recipient_list = [settings.EMAIL_OVERRIDE_ADDRESS]
                self.stdout.write(f"⚠️ TEST MODE: Redirecting Escalation Email to {settings.EMAIL_OVERRIDE_ADDRESS}")
            else:
                # PRODUCTION: Send to Senior Officials
                # For now, we default to AMC City, but logic could be smarter based on Ward location
                recipient_list = [settings.SENIOR_OFFICIALS['AMC_CITY']]

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            self.stdout.write(f"📧 Sent escalation email for Complaint #{complaint.id}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to send email for #{complaint.id}: {e}"))
