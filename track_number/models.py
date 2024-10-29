from django.db import models


class TrackNumber(models.Model):
    track = models.CharField(max_length=50, unique=True, primary_key=True)
    status = models.CharField(max_length=30)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]
