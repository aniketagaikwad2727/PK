from django.db import models
from django.contrib.auth.models import User
from therapy.models import Therapist, Therapy
from patients.models import Patient


# =====================================================
# PATIENT APPOINTMENT
# =====================================================
class PatientAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True)

    date = models.DateField()
    time = models.TimeField()

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} – {self.therapy.name} on {self.date}"


# =====================================================
# THERAPIST APPOINTMENT MIRROR TABLE
# =====================================================
class TherapistAppointment(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.therapist.full_name} – {self.date}"


# =====================================================
# THERAPY SESSION LOG
# =====================================================
class TherapySession(models.Model):
    appointment = models.OneToOneField(
    PatientAppointment, on_delete=models.CASCADE, null=True, blank=True
    )
    therapist = models.ForeignKey(
        Therapist, on_delete=models.SET_NULL, null=True, blank=True
    )
    therapy = models.ForeignKey(
        Therapy, on_delete=models.SET_NULL, null=True, blank=True
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, blank=True
    )
    session_date = models.DateField(null=True, blank=True)
    session_start = models.TimeField(null=True, blank=True)
    session_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Session: {self.patient.full_name} on {self.session_date}"
