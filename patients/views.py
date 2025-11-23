from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Patient
from users.models import UserProfile


# ============================
# PROFILE PAGE
# ============================
def profile(request):
    return render(request, 'patient_portal/profile.html')


# ============================
# APPOINTMENTS PAGE (DISABLED)
# ============================
def appointments(request):
    return render(request, 'patient_portal/appointments.html', {
        "therapies": [],
        "therapists": [],
        "upcoming": [],
        "history": []
    })


def cancel_appointment(request, appt_id):
    messages.error(request, "Appointment system not yet connected.")
    return redirect('appointments')


def slots_api(request):
    return JsonResponse({"slots": []})


# ============================
# DASHBOARD
# ============================
def dashboard(request):
    return render(request, 'patient_portal/dashboard.html', {
        "upcoming": [],
        "previous": [],
    })


# ============================
# BILLING PAGE (DISABLED)
# ============================
def billing(request):
    return render(request, "patient_portal/billing.html", {
        "pending": [],
        "history": []
    })


def mark_paid(request, invoice_id):
    messages.error(request, "Billing system not yet connected.")
    return redirect("billing")


# ============================
# LOGIN PAGE
# ============================
def auth_page(request):
    return render(request, "login.html")


# ============================
# SIGNUP API
# ============================
@method_decorator(csrf_exempt, name='dispatch')
class SignupAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "patient")

        dob = data.get("dob")
        gender = data.get("gender")
        address = data.get("address")
        allergies = data.get("allergies")
        contact = data.get("pat_contact_number")

        if not email or not password or not full_name:
            return Response({"error": "Required fields missing"}, status=400)

        if User.objects.filter(username=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        # Create user profile
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            role=role
        )

        # Save Patient details
        if role == "patient":
            Patient.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                gender=gender,
                address=address,
                allergies=allergies,
                date_of_birth=dob,
                pat_contact_number=contact
            )

        return Response({"message": "Account created successfully!"}, status=201)


# ============================
# LOGIN API
# ============================
@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        login(request, user)
        role = user.profile.role

        # Redirect based on role
        if role == "patient":
            return Response({
                "message": "Login successful",
                "role": role,
                "redirect": "/patient/dashboard/"
            })

        if role == "admin":
            return Response({
                "message": "Login successful",
                "role": role,
                "redirect": "/admin/"
            })

        if role == "therapist":
            return Response({
                "message": "Login successful",
                "role": role,
                "redirect": "/sessions/list/"
            })

        return Response({
            "message": "Login successful",
            "role": role,
            "redirect": "/"
        })
