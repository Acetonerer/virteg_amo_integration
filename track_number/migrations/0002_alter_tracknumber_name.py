# Generated by Django 5.1.2 on 2024-10-30 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("track_number", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tracknumber",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
