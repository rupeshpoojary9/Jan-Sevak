from django.core.management.base import BaseCommand
from complaints.models import Complaint, ComplaintImage
import os

class Command(BaseCommand):
    help = 'Deletes all complaints and associated media files'

    def handle(self, *args, **options):
        self.stdout.write("🗑️  Deleting all complaints and media...")

        # 1. Delete ComplaintImage files
        try:
            images = ComplaintImage.objects.all()
            for img in images:
                if img.image:
                    try:
                        if os.path.isfile(img.image.path):
                            os.remove(img.image.path)
                            self.stdout.write(f"Deleted file: {img.image.path}")
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Could not delete image file {img.image}: {e}"))
        except Exception as e:
             self.stdout.write(self.style.WARNING(f"Could not access ComplaintImage (might not exist yet): {e}"))
        
        # 2. Delete Complaint main images
        complaints = Complaint.objects.all()
        for c in complaints:
            if c.image:
                try:
                    if os.path.isfile(c.image.path):
                        os.remove(c.image.path)
                        self.stdout.write(f"Deleted file: {c.image.path}")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Could not delete file {c.image}: {e}"))

        # 3. Delete Database Records
        count = complaints.count()
        complaints.delete() # Cascades to ComplaintImage and Verification

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully deleted {count} complaints and cleaned up files."))
