from django.db import models
from django.contrib.auth.models import User


# =====================================================
# THERAPY CATEGORY (Optional)
# Example: Panchakarma, Ayurvedic Massage, Detox
# =====================================================
class TherapyCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =====================================================
# THERAPY MODEL
# Example: Vamana, Virechana, Nasya, Basti, Raktamokshana
# =====================================================
class Therapy(models.Model):
    category = models.ForeignKey(TherapyCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(default=60)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name


# =====================================================
# THERAPIST MODEL
# =====================================================
class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    
    specialization = models.CharField(max_length=200, blank=True)
    expertise = models.TextField(blank=True)   # e.g. "Vamana, Basti, Nasya"
    experience_years = models.IntegerField(default=0)

    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


# =====================================================
# OPTIONAL: THERAPIST AVAILABILITY
# Useful for slot booking system
# =====================================================
class TherapistAvailability(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.therapist.full_name} - {self.date}"
