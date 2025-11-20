from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('patient-dashboard/', lambda request: render(request, 'patient_portal/patient-dashboard.html')),
]
