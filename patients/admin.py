from django.contrib import admin
from .models import Patient, Therapy, Therapist, PatientAppointment, TherapistAppointment ,Notification

admin.site.register(Patient)
admin.site.register(Therapy)
admin.site.register(Therapist)
admin.site.register(PatientAppointment)
admin.site.register(TherapistAppointment)
from django.contrib import admin

admin.site.register(Notification)
from .models import Billing

admin.site.register(Billing)

