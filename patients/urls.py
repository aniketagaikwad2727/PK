from django.urls import path
from . import views

urlpatterns = [

    # Patient Dashboard
    path("dashboard/", views.dashboard, name="patient_dashboard"),

    # Profile Page
    path("profile/", views.profile, name="profile"),

    # Appointments (disabled version)
    path("appointments/", views.appointments, name="appointments"),
    path("appointments/cancel/<int:appt_id>/", views.cancel_appointment, name="cancel_appointment"),
    path("appointments/slots/", views.slots_api, name="slots_api"),

    # Billing
    path("billing/", views.billing, name="billing"),
    path("billing/mark-paid/<str:invoice_id>/", views.mark_paid, name="mark_paid"),
]
