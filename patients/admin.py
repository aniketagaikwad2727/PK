from django.contrib import admin
from .models import Patient, Therapy, Therapist, PatientAppointment, TherapistAppointment

admin.site.register(Patient)
admin.site.register(Therapy)
admin.site.register(Therapist)
admin.site.register(PatientAppointment)
admin.site.register(TherapistAppointment)
