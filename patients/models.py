from django.db import models

class Patient(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Therapy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Therapist(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class PatientAppointment(models.Model):
    patient_name = models.CharField(max_length=100)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)   # <-- FIXED

    def __str__(self):
        return f"{self.patient_name} - {self.therapy} - {self.date}"


class TherapistAppointment(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)   # <-- FIXED

    def __str__(self):
        return f"{self.therapist} - {self.patient_name} - {self.date}"


# notification   
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    

class Billing(models.Model):
    patient = models.CharField(max_length=150)
    invoice_id = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")  # Pending / Paid
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_id} - {self.patient}"
    



