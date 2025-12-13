from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Ward(models.Model):
    """
    Represents an administrative ward in Mumbai (e.g., A, G/North).
    """
    name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    officer_email = models.EmailField(help_text="Email of the Assistant Municipal Commissioner")
    
    def __str__(self):
        return f"{self.name} - {self.full_name}"

class Complaint(models.Model):
    class Category(models.TextChoices):
        POTHOLE = 'POTHOLE', _('Pothole')
        GARBAGE = 'GARBAGE', _('Garbage/Debris')
        DRAINAGE = 'DRAINAGE', _('Drainage/Flooding')
        LIGHTING = 'LIGHTING', _('Street Lighting')
        WATER = 'WATER', _('Water Supply')
        SANITATION = 'SANITATION', _('Public Toilets/Sanitation')
        TRAFFIC = 'TRAFFIC', _('Traffic/Parking')
        PARKS = 'PARKS', _('Parks/Gardens')
        OTHERS = 'OTHERS', _('Others')

    class Status(models.TextChoices):
        NEW = 'NEW', _('New')
        VERIFIED = 'VERIFIED', _('Community Verified')
        ESCALATED = 'ESCALATED', _('Escalated to Official')
        RESOLVED = 'RESOLVED', _('Resolved')
        REOPENED = 'REOPENED', _('Reopened')

    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    
    # Core Data
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHERS)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_address = models.CharField(max_length=255, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)

    # AI & Meta
    from django.core.validators import MinValueValidator, MaxValueValidator
    urgency_score = models.IntegerField(default=0, help_text="AI calculated score 1-10", validators=[MinValueValidator(0), MaxValueValidator(10)])
    ai_verified_category = models.BooleanField(default=False, help_text="True if AI image analysis matches category")
    
    # Community
    verification_count = models.PositiveIntegerField(default=0)
    
    # Resolution Workflow
    admin_token = models.UUIDField(default=uuid.uuid4, editable=False)
    user_confirmed = models.BooleanField(default=False)
    escalation_level = models.IntegerField(default=0, help_text="0=Ward, 1=Zone, 2=Commissioner")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} in {self.ward} ({self.status})"

class Verification(models.Model):
    """
    Tracks community upvotes to prevent spam.
    """
    complaint = models.ForeignKey(Complaint, related_name='verifications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('complaint', 'user')

class UserProfile(models.Model):
    """
    Gamification profile for citizens.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0)
    badges = models.JSONField(default=list, blank=True) # List of strings e.g. ["Pothole Hunter"]

    def __str__(self):
        return f"{self.user.username} ({self.points} pts)"