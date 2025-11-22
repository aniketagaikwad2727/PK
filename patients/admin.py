from django.contrib import admin
from .models import (
    Patient,
    Therapy,
    Therapist,
    PatientAppointment,
    TherapistAppointment,
    Notification,
    Billing
)

admin.site.register(Patient)
admin.site.register(Therapy)
admin.site.register(Therapist)
admin.site.register(PatientAppointment)
admin.site.register(TherapistAppointment)
admin.site.register(Notification)
admin.site.register(Billing)
