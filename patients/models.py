from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    pat_contact_number = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.full_name
