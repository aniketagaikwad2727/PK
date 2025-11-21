from django.urls import path
from .views import auth_page, SignupAPI, LoginAPI, patient_dashboard, landing_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', auth_page, name='auth-page'),
    path('signup/', SignupAPI.as_view(), name='signup'),
    path('login/', LoginAPI.as_view(), name='login'),
    path("patient-dashboard/", patient_dashboard, name="patient_dashboard"),
]
