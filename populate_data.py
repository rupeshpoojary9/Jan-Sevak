import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from django.contrib.auth.models import User
from complaints.models import Complaint, Ward, Verification

def run():
    print("🧹 Cleaning up old complaints...")
    Complaint.objects.all().delete()
    Verification.objects.all().delete()
    
    # Check Wards
    if Ward.objects.count() == 0:
        print("⚠️ No wards found. Please run 'python populate_wards.py' first.")
        return

    print("👥 Creating sample users...")
    users = []
    usernames = ['priya_sharma', 'rahul_desai', 'amit_patil', 'sneha_k', 'vikram_s', 'arjun_m', 'zoya_khan']
    for username in usernames:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('password123')
            user.save()
        users.append(user)

    print("📝 Generating realistic complaints...")
    
    wards = list(Ward.objects.all())
    
    complaint_templates = [
        {
            "title": "Deep Pothole on Main Road",
            "desc": "There is a very deep pothole in the middle of the road causing traffic jams and accidents. It has been here for weeks and is getting bigger with the rain. Please fix immediately.",
            "cat": "POTHOLE",
            "urgency": 8
        },
        {
            "title": "Garbage Dump Not Cleared",
            "desc": "The garbage bin has been overflowing for 3 days. It smells terrible and is attracting stray dogs and rats. Health hazard for the colony.",
            "cat": "GARBAGE",
            "urgency": 7
        },
        {
            "title": "Street Light Not Working",
            "desc": "The street light near the park entrance has been flickering and is now completely off. It's unsafe for women and children walking at night.",
            "cat": "LIGHTING",
            "urgency": 6
        },
        {
            "title": "Water Leakage in Pipeline",
            "desc": "Clean water is getting wasted due to a burst pipe near the market area. Thousands of liters are being wasted while we face water cuts.",
            "cat": "WATER",
            "urgency": 9
        },
        {
            "title": "Illegal Parking Blocking Footpath",
            "desc": "Cars and bikes are parked on the footpath forcing pedestrians to walk on the busy road. This is very dangerous, especially for school kids.",
            "cat": "TRAFFIC",
            "urgency": 5
        },
        {
            "title": "Public Toilet Unusable",
            "desc": "The public toilet near the station is in a pathetic state. No water, broken doors, and very dirty. It needs immediate cleaning and repair.",
            "cat": "SANITATION",
            "urgency": 8
        },
        {
            "title": "Broken Swings in Park",
            "desc": "The children's play area has broken swings and rusted slides. A child got hurt yesterday. Please maintain the park equipment.",
            "cat": "PARKS",
            "urgency": 5
        },
        {
            "title": "Clogged Drain Causing Flooding",
            "desc": "Even with light rain, the road gets flooded because the drains are completely choked with plastic and debris. Mosquito breeding ground.",
            "cat": "DRAINAGE",
            "urgency": 8
        },
        {
            "title": "Dead Animal on Road",
            "desc": "There is a dead dog on the side of the road. It is starting to decompose and smell. Please arrange for removal.",
            "cat": "GARBAGE",
            "urgency": 6
        },
        {
            "title": "Manhole Cover Missing",
            "desc": "A manhole cover is missing on the footpath. It is a death trap for pedestrians, especially at night. Someone put a branch in it as a warning.",
            "cat": "DRAINAGE",
            "urgency": 10
        }
    ]

    # Mumbai Coordinates (Approx Center)
    base_lat = 19.0760
    base_lng = 72.8777

    for i in range(25): # Create 25 complaints
        template = random.choice(complaint_templates)
        ward = random.choice(wards)
        reporter = random.choice(users)
        is_anon = random.choice([True, False, False, False]) # 25% anonymous
        
        # Randomize location slightly (spread across Mumbai)
        lat = base_lat + random.uniform(-0.08, 0.08)
        lng = base_lng + random.uniform(-0.08, 0.08)
        
        # Random Status
        status_choices = ['NEW', 'NEW', 'VERIFIED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']
        status = random.choice(status_choices)
        
        c = Complaint.objects.create(
            title=template['title'],
            description=template['desc'],
            category=template['cat'],
            ward=ward,
            reporter=reporter if not is_anon else None,
            is_anonymous=is_anon,
            latitude=lat,
            longitude=lng,
            location_address=f"Near {ward.full_name}, Mumbai",
            urgency_score=min(10, max(1, template['urgency'] + random.randint(-1, 1))),
            status=status,
            ai_verified_category=True,
            verification_count=random.randint(0, 150)
        )
        
        # Backdate creation time
        days_ago = random.randint(0, 10)
        hours_ago = random.randint(0, 23)
        c.created_at = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
        c.save()

    print("✅ Successfully created 25 sample complaints!")

if __name__ == '__main__':
    run()
