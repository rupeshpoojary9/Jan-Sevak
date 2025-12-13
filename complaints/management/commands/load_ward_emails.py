from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads the Ward email data from the fixture'

    def handle(self, *args, **options):
        self.stdout.write("📥 Loading Ward Emails...")
        
        import json
        from complaints.models import Ward

        fixture_path = os.path.join(settings.BASE_DIR, 'ward_emails.json')
        
        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f"❌ Fixture not found at {fixture_path}"))
            return

        try:
            with open(fixture_path, 'r') as f:
                data = json.load(f)
                
            count = 0
            for item in data:
                fields = item['fields']
                ward, created = Ward.objects.update_or_create(
                    name=fields['name'],
                    defaults={
                        'full_name': fields['full_name'],
                        'officer_email': fields['officer_email']
                    }
                )
                count += 1
                
            self.stdout.write(self.style.SUCCESS(f"✅ Successfully updated {count} Wards with official emails!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to load data: {e}"))
