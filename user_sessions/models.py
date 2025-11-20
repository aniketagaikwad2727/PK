from django.db import models
from patients.models import Patient
from therapy.models import Therapist
from inventory.models import InventoryItem


class TherapySession(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    session_type = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    symptoms_score = models.IntegerField(null=True, blank=True)
    progress_summary = models.TextField(blank=True)

    is_completed = models.BooleanField(default=False)
    consent_signed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.date}"


class SessionInventoryUsage(models.Model):
    session = models.ForeignKey(TherapySession, on_delete=models.CASCADE, related_name="inventory")
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_used = models.FloatField()

    used_at = models.DateTimeField(auto_now_add=True)
