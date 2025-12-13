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

# 4. Send Email Notification to Ward Officer
@receiver(post_save, sender=Complaint)
def send_complaint_email(sender, instance, created, **kwargs):
    if created and instance.ward and instance.ward.officer_email:
        # Generate Magic Link
        # In production, use request.build_absolute_uri or settings.SITE_URL
        resolve_link = f"http://127.0.0.1:8000/api/resolve/{instance.id}/{instance.admin_token}/"
        
        subject = f"[URGENT] Formal Grievance: {instance.category} in Ward {instance.ward.name} - Ref #{instance.id}"
        message = f"""
        FORMAL CITIZEN GRIEVANCE
        Date: {instance.created_at.strftime('%Y-%m-%d')}
        Reference No: #{instance.id}
        Urgency Score: {instance.urgency_score}/10 (AI Assessed)

        Dear Assistant Municipal Commissioner,

        This is to bring to your immediate attention a civic issue reported by a citizen in your jurisdiction, under Ward {instance.ward.name} ({instance.ward.full_name}).

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
        (System-generated report verified by AI)
        """
        
        try:
            # FOR TESTING: Send to dummy email as requested
            recipient_list = ["poojary.rupesh12@gmail.com"]
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            print(f"Email sent to {recipient_list[0]}")
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
            # FOR TESTING: Send to dummy email
            recipient_list = ["poojary.rupesh12@gmail.com"]
            # In production: recipient_list = [instance.reporter.email]
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            print(f"Resolution Email sent to {recipient_list[0]}")
        except Exception as e:
            print(f"Failed to send resolution email: {e}")
