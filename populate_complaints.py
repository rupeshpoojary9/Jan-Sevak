import random
from django.contrib.auth.models import User
from complaints.models import Complaint, Ward

def create_complaints():
    # Ensure we have a user
    user, _ = User.objects.get_or_create(username='test_generator', defaults={'email': 'gen@test.com'})
    
    # Get all wards
    wards = list(Ward.objects.all())
    if not wards:
        print("No wards found! Please run populate_wards.py first.")
        return

    categories = [c[0] for c in Complaint.Category.choices]
    statuses = [s[0] for s in Complaint.Status.choices]
    
    titles = [
        "Huge Pothole on Main Road", "Garbage not collected for days", "Street light flickering",
        "Drainage overflowing", "Broken footpath", "Illegal parking blocking way",
        "Water leakage in pipeline", "Dead animal on street", "Tree branch about to fall",
        "Construction debris dumped"
    ]
    
    print(f"Generating 30 complaints...")
    
    for i in range(30):
        ward = random.choice(wards)
        category = random.choice(categories)
        status = random.choice(statuses)
        title = random.choice(titles) + f" - {i+1}"
        
        # Random location around Mumbai (approx)
        lat = 19.0 + random.uniform(0, 0.2)
        lng = 72.8 + random.uniform(0, 0.2)
        
        Complaint.objects.create(
            title=title,
            description=f"This is a test complaint number {i+1}. Please attend to this issue immediately.",
            category=category,
            status=status,
            ward=ward,
            reporter=user,
            latitude=lat,
            longitude=lng,
            location_address=f"Near {ward.full_name} Station",
            urgency_score=random.randint(1, 10),
            verification_count=random.randint(0, 50)
        )
        
    print("Successfully created 30 complaints!")

create_complaints()
