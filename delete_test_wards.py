import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.models import Ward

OFFICIAL_WARDS = [
    'A', 'B', 'C', 'D', 'E', 
    'F/South', 'F/North', 
    'G/South', 'G/North', 
    'H/East', 'H/West', 
    'K/East', 'K/West', 
    'P/South', 'P/North', 
    'R/South', 'R/North', 'R/Central', 
    'L', 'M/East', 'M/West', 'N', 'S', 'T'
]

def delete_test_wards():
    print("Checking for Test Wards...")
    all_wards = Ward.objects.all()
    deleted_count = 0
    
    for ward in all_wards:
        if ward.name not in OFFICIAL_WARDS:
            print(f"Deleting Test Ward: {ward.name} (ID: {ward.id})")
            ward.delete()
            deleted_count += 1
        else:
            # Optional: Check for duplicates of official wards
            pass
            
    print(f"\nDeleted {deleted_count} test wards.")
    print(f"Remaining Wards: {Ward.objects.count()}")

if __name__ == "__main__":
    delete_test_wards()
