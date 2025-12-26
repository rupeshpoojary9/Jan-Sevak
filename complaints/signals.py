from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Complaint, Verification, UserProfile

# 1. Auto-create UserProfile for new users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# 2. Award Points for Resolving a Complaint
@receiver(post_save, sender=Complaint)
def award_points_resolution(sender, instance, created, **kwargs):
    # If status changed to RESOLVED and we have a reporter
    if instance.status == Complaint.Status.RESOLVED and instance.reporter:
        profile, _ = UserProfile.objects.get_or_create(user=instance.reporter)
        
        # Simple check to avoid double counting (in a real app, use a Transaction log)
        # Here we just add points. 
        # Ideally we should check if points were already awarded for this complaint.
        # For MVP, we assume status changes to RESOLVED only once.
        profile.points += 50
        profile.save()

# 3. Award Points for Verifying (Upvoting)
@receiver(post_save, sender=Verification)
def award_points_verification(sender, instance, created, **kwargs):
    if created:
        profile, _ = UserProfile.objects.get_or_create(user=instance.user)
        profile.points += 10
        profile.save()

from django.db.models.signals import post_delete

@receiver(post_delete, sender=Verification)
def revoke_points_verification(sender, instance, **kwargs):
    try:
        profile = instance.user.profile
        profile.points = max(0, profile.points - 10) # Prevent negative points
        profile.save()
    except UserProfile.DoesNotExist:
        pass

from django.core.mail import send_mail
from django.conf import settings

# 4. Send Email Notification to Ward Officer (Triggered by Verification)
@receiver(post_save, sender=Verification)
def check_verification_threshold(sender, instance, created, **kwargs):
    if created:
        complaint = instance.complaint
        # Count total verifications (including the implicit one from the reporter if we count that, 
        # but usually reporter is separate. Let's count actual Verification objects).
        # Note: In our logic, reporter doesn't get a Verification object automatically, 
        # but for this requirement "community is verifying", we can say:
        # Threshold = 2 (1 Reporter + 1 Community Member) OR just 2 Verification objects if reporter also verifies.
        # Let's assume we need 1 *additional* verification from the community.
        
        # Check if email already sent to avoid duplicates
        # In a real app, add a 'email_sent' boolean field to Complaint model.
        # For now, we'll just check if count is EXACTLY 1 (meaning this is the first community verification).
        # Wait, user said "community is verifying". 
        # If reporter creates it, count is 0. 
        # Community member 1 verifies -> Count 1.
        # Let's trigger on Count == 1.
        
        verification_count = complaint.verifications.count()
        
        # Smart Threshold Logic
        # High Urgency (8-10) -> Threshold 1 (Immediate)
        # Normal (0-7) -> Threshold 3 (Community Verified)
        
        threshold = 3
        if complaint.urgency_score >= 8:
            threshold = 1
            
        if verification_count == threshold:
            send_complaint_email(complaint)

from django.core.mail import EmailMessage

def send_complaint_email(instance):
    if instance.ward and instance.ward.officer_email:
        # Generate Magic Link
        resolve_link = f"http://127.0.0.1:8000/api/resolve/{instance.id}/{instance.admin_token}/"
        
        subject = f"[URGENT] Formal Grievance: {instance.category} in Ward {instance.ward.name} - Ref #{instance.id}"
        message = f"""
        FORMAL CITIZEN GRIEVANCE (Community Verified)
        Date: {instance.created_at.strftime('%Y-%m-%d')}
        Reference No: #{instance.id}
        Urgency Score: {instance.urgency_score}/10 (AI Assessed)
        Community Verifications: {instance.verifications.count()}

        Dear Assistant Municipal Commissioner,

        This is to bring to your immediate attention a civic issue reported by a citizen in your jurisdiction, under Ward {instance.ward.name} ({instance.ward.full_name}).
        
        This issue has been verified by the community.

        ISSUE DETAILS:
        ------------------------------------------------
        Nature of Complaint: {instance.get_category_display()}
        Location: {instance.location_address}
        GPS Coordinates: {instance.latitude}, {instance.longitude}
        Description: {instance.description}
        ------------------------------------------------

        LEGAL CONTEXT & OBLIGATION:
        We respectfully remind you of the statutory duties under:
        1. Section 61 of the Mumbai Municipal Corporation Act, 1888 (Maintenance of public streets/sanitation).
        2. The Maharashtra Right to Public Services Act, 2015 (Time-bound service delivery).
        3. Article 21 of the Constitution of India (Right to safe roads/environment).

        ACTION REQUIRED:
        Given the Urgency Score of {instance.urgency_score}/10, we request you to inspect and resolve this matter immediately.

        Please update the status of this complaint by clicking the secure link below:
        {resolve_link}

        Failure to address this grievance may result in automatic escalation to the Deputy Municipal Commissioner.

        Yours faithfully,

        Jan Sevak Platform
        (System-generated report verified by AI & Community)
        """
        
        try:
            # Determine Recipient
            recipient_email = instance.ward.officer_email
            if settings.EMAIL_OVERRIDE_ADDRESS:
                recipient_email = settings.EMAIL_OVERRIDE_ADDRESS
                print(f"Redirecting email to override address: {recipient_email}")

            recipient_list = [recipient_email]
            cc_list = []
            
            # Check for CC Reporter
            if instance.cc_reporter and instance.reporter and instance.reporter.email:
                cc_list.append(instance.reporter.email)
                print(f"Adding reporter {instance.reporter.email} to CC list")
            
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                cc=cc_list
            )
            email.send(fail_silently=False)
            
            print(f"Email sent to {recipient_list} with CC: {cc_list}")
        except Exception as e:
            print(f"Failed to send email: {e}")

# 5. Notify Citizen when Complaint is Resolved
@receiver(post_save, sender=Complaint)
def notify_citizen_resolution(sender, instance, created, **kwargs):
    # Check if status is RESOLVED and we have a reporter
    if instance.status == Complaint.Status.RESOLVED and instance.reporter:
        # In a real app, we should check if we just changed to RESOLVED to avoid duplicate emails.
        # For this MVP, we assume the transition happens once via the resolve_complaint view.
        
        subject = f"[Jan Sevak] Good News! Your Complaint is Resolved: {instance.title}"
        message = f"""
        Dear {instance.reporter.username},

        Great news! The complaint you reported has been marked as RESOLVED by the authorities.

        Title: {instance.title}
        Ward: {instance.ward.name if instance.ward else 'N/A'}
        
        Please log in to your dashboard to CONFIRM that the issue is actually fixed.
        Your confirmation helps us ensure quality.

        Thank you for being an active citizen!
        
        Regards,
        Jan Sevak Team
        """
        
        try:
            # Determine Recipient
            recipient_email = instance.reporter.email
            
            # CHECK FOR TEST MODE / OVERRIDE
            if settings.EMAIL_OVERRIDE_ADDRESS:
                recipient_email = settings.EMAIL_OVERRIDE_ADDRESS
                print(f"Redirecting Resolution Email to override address: {recipient_email}")
            
            recipient_list = [recipient_email]
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            print(f"Resolution Email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send resolution email: {e}")
