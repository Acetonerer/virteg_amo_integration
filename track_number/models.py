from django.db import models


class TrackNumber(models.Model):
    track = models.CharField(max_length=50, unique=True, primary_key=True)
    status = models.CharField(max_length=30)
    # lead_id = models.BigIntegerField(primary_key=True)
    message_type = models.CharField(max_length=10)
    language = models.CharField(max_length=10, default='RUS')
    pass
