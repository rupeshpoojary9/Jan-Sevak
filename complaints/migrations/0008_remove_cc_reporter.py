# Generated manually

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0007_alter_complaint_latitude_alter_complaint_longitude_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE complaints_complaint DROP COLUMN IF EXISTS cc_reporter;",
            reverse_sql="ALTER TABLE complaints_complaint ADD COLUMN cc_reporter varchar(255) NULL;" # Best guess for reverse
        ),
    ]
