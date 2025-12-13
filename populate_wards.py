import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

from complaints.models import Ward

wards_data = [
    # City
    {"name": "A", "full_name": "Colaba / Churchgate", "officer_email": "wardA@mcgm.gov.in"},
    {"name": "B", "full_name": "Sandhurst Road", "officer_email": "wardB@mcgm.gov.in"},
    {"name": "C", "full_name": "Marine Lines", "officer_email": "wardC@mcgm.gov.in"},
    {"name": "D", "full_name": "Grant Road", "officer_email": "wardD@mcgm.gov.in"},
    {"name": "E", "full_name": "Byculla", "officer_email": "wardE@mcgm.gov.in"},
    
    # Western Suburbs
    {"name": "H/West", "full_name": "Bandra West", "officer_email": "wardHW@mcgm.gov.in"},
    {"name": "H/East", "full_name": "Bandra East", "officer_email": "wardHE@mcgm.gov.in"},
    {"name": "K/West", "full_name": "Andheri West", "officer_email": "wardKW@mcgm.gov.in"},
    {"name": "K/East", "full_name": "Andheri East", "officer_email": "wardKE@mcgm.gov.in"},
    {"name": "P/South", "full_name": "Goregaon", "officer_email": "wardPS@mcgm.gov.in"},
    {"name": "P/North", "full_name": "Malad", "officer_email": "wardPN@mcgm.gov.in"},
    {"name": "R/South", "full_name": "Kandivali", "officer_email": "wardRS@mcgm.gov.in"},
    {"name": "R/Central", "full_name": "Borivali", "officer_email": "wardRC@mcgm.gov.in"},
    {"name": "R/North", "full_name": "Dahisar", "officer_email": "wardRN@mcgm.gov.in"},

    # Eastern Suburbs
    {"name": "L", "full_name": "Kurla", "officer_email": "wardL@mcgm.gov.in"},
    {"name": "M/East", "full_name": "Govandi", "officer_email": "wardME@mcgm.gov.in"},
    {"name": "M/West", "full_name": "Chembur", "officer_email": "wardMW@mcgm.gov.in"},
    {"name": "N", "full_name": "Ghatkopar", "officer_email": "wardN@mcgm.gov.in"},
    {"name": "S", "full_name": "Bhandup", "officer_email": "wardS@mcgm.gov.in"},
    {"name": "T", "full_name": "Mulund", "officer_email": "wardT@mcgm.gov.in"},
    
    # Central
    {"name": "F/North", "full_name": "Matunga", "officer_email": "wardFN@mcgm.gov.in"},
    {"name": "F/South", "full_name": "Parel", "officer_email": "wardFS@mcgm.gov.in"},
    {"name": "G/North", "full_name": "Dadar / Dharavi", "officer_email": "wardGN@mcgm.gov.in"},
    {"name": "G/South", "full_name": "Worli", "officer_email": "wardGS@mcgm.gov.in"},

    # Extended Regions (MBMC, TMC, NMMC)
    {"name": "MBMC", "full_name": "Mira-Bhayandar", "officer_email": "commissioner@mbmc.gov.in"},
    {"name": "TMC", "full_name": "Thane", "officer_email": "mc@thanecity.gov.in"},
    {"name": "NMMC", "full_name": "Navi Mumbai", "officer_email": "commissioner@nmmc.gov.in"},
]

for data in wards_data:
    Ward.objects.get_or_create(name=data["name"], defaults=data)
    print(f"Ensured Ward: {data['name']}")
