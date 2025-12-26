from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes all non-superuser accounts'

    def handle(self, *args, **options):
        self.stdout.write("👥 Deleting regular users...")
        
        # Filter non-superusers
        users = User.objects.filter(is_superuser=False)
        count = users.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING("⚠️  No regular users found to delete."))
            return

        # Delete
        users.delete()
        
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully deleted {count} users."))
