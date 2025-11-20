from rest_framework import serializers
from .models import TherapySession, SessionInventoryUsage

class TherapySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapySession
        fields = "__all__"


class SessionInventoryUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionInventoryUsage
        fields = "__all__"
