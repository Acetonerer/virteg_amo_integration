from rest_framework import serializers
from .models import TrackNumber


class TrackNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackNumber
        fields = ['track', 'status', 'language']
