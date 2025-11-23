from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "gender", "date_of_birth")
    search_fields = ("full_name", "email")
