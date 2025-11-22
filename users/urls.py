from django.urls import path
from .views import (
    auth_page, SignupAPI, LoginAPI, 
    patient_dashboard, landing_page
)

urlpatterns = [
    path('', landing_page, name='landing'),

    # Page route (HTML)
    path('login/', auth_page, name='auth-page'),

    # API routes
    path('api/signup/', SignupAPI.as_view(), name='signup'),
    path('api/login/', LoginAPI.as_view(), name='login'),

    # Dashboard
    path("patient-dashboard/", patient_dashboard, name="patient_dashboard"),
]
