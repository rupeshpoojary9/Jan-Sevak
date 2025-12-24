import os
import django
import random
from django.contrib.auth.models import User
from complaints.models import Complaint, Ward

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

def populate():
    print("🚀 Populating Realistic Dummy Data...")

    # 1. Create/Get Wards
    wards_data = [
        {'name': 'A', 'full_name': 'Colaba, Fort', 'lat': 18.9220, 'lon': 72.8347},
        {'name': 'G/N', 'full_name': 'Dadar, Dharavi', 'lat': 19.0178, 'lon': 72.8478},
        {'name': 'H/W', 'full_name': 'Bandra West', 'lat': 19.0596, 'lon': 72.8295},
        {'name': 'K/E', 'full_name': 'Andheri East', 'lat': 19.1136, 'lon': 72.8697},
        {'name': 'S', 'full_name': 'Powai, Bhandup', 'lat': 19.1176, 'lon': 72.9060},
    ]
    
    wards = []
    for w in wards_data:
        ward, _ = Ward.objects.get_or_create(
            name=w['name'], 
            defaults={'full_name': w['full_name'], 'officer_email': 'admin@jansevak.com'}
        )
        wards.append((ward, w['lat'], w['lon']))
        print(f"✅ Ward {w['name']} ready.")

    # 2. Create Reporter
    reporter, _ = User.objects.get_or_create(username='citizen_user', email='citizen@test.com')
    if not reporter.check_password('pass'):
        reporter.set_password('pass')
        reporter.save()

    # 3. Complaints Data
    complaint_templates = [
        {
            'title': 'Huge Pothole on SV Road',
            'desc': 'Deep pothole causing traffic slowdown near the junction. Dangerous for bikers.',
            'cat': 'POTHOLE',
            'urgency': 8
        },
        {
            'title': 'Garbage Pileup near Station',
            'desc': 'Uncollected garbage for 3 days. Foul smell spreading.',
            'cat': 'GARBAGE',
            'urgency': 9
        },
        {
            'title': 'Street Light Not Working',
            'desc': 'Dark stretch of road, unsafe for pedestrians at night.',
            'cat': 'LIGHTING',
            'urgency': 5
        },
        {
            'title': 'Choked Drainage',
            'desc': 'Water logging even after light rain due to clogged drains.',
            'cat': 'DRAINAGE',
            'urgency': 7
        },
        {
            'title': 'Illegal Parking Blocking Footpath',
            'desc': 'Cars parked on footpath forcing people to walk on road.',
            'cat': 'TRAFFIC',
            'urgency': 4
        },
        {
            'title': 'Broken Park Bench',
            'desc': 'Bench in the public garden is broken.',
            'cat': 'PARKS',
            'urgency': 2
        }
    ]

    # 4. Create Complaints
    count = 0
    for i in range(15): # Create 15 complaints
        ward, base_lat, base_lon = random.choice(wards)
        template = random.choice(complaint_templates)
        
        # Add small random variation to location so they don't overlap perfectly
        lat_offset = random.uniform(-0.01, 0.01)
        lon_offset = random.uniform(-0.01, 0.01)
        
        Complaint.objects.create(
            title=template['title'],
            description=template['desc'],
            category=template['cat'],
            ward=ward,
            reporter=reporter,
            location_address=f"Near {ward.full_name}",
            latitude=base_lat + lat_offset,
            longitude=base_lon + lon_offset,
            urgency_score=template['urgency'],
            status='NEW' # No email trigger
        )
        count += 1
        
    print(f"✅ Created {count} realistic complaints across Mumbai.")

populate()
