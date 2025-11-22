from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('billing/', views.billing, name='billing'),
    path('profile/', views.profile, name='profile'),
]
