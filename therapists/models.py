from django.db import models
from django.contrib.auth.models import User


class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    license_no = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=150, blank=True)

    # store as comma separated values — e.g. "Vamana, Basti, Nasya"
    expertise = models.TextField(blank=True)

    def __str__(self):
        return self.name
