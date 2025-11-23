from django.urls import path
from .views import (
    SignupAPI,
    LoginAPI,
    patient_dashboard,
    therapist_dashboard,
    admin_dashboard,
)

urlpatterns = [
    # API endpoints (called from login.html via JS)
    path("signup/", SignupAPI.as_view(), name="api-signup"),
    path("login/", LoginAPI.as_view(), name="api-login"),

    # role dashboards (these URLs are under /api/auth/..., but you can also move them if you want)
    path("patient-dashboard/", patient_dashboard, name="patient_dashboard"),
    path("therapist-dashboard/", therapist_dashboard, name="therapist_dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
]
