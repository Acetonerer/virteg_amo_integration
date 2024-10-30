# Generated by Django 5.1.2 on 2024-10-30 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("track_number", "0002_alter_tracknumber_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tracknumber",
            old_name="name",
            new_name="name_recip",
        ),
        migrations.AddField(
            model_name="tracknumber",
            name="name_sender",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
