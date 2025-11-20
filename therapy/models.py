from django.db import models

# Create your models here.
from django.db import models

class Therapist(models.Model):
    full_name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=True)

    def __str__(self):
        return self.full_name
