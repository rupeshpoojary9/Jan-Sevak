import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.models import Ward

def list_wards():
    print(f"{'ID':<5} {'Name':<10} {'Full Name':<30} {'Email'}")
    print("-" * 80)
    for ward in Ward.objects.all().order_by('id'):
        print(f"{ward.id:<5} {ward.name:<10} {ward.full_name:<30} {ward.officer_email}")

if __name__ == "__main__":
    list_wards()
