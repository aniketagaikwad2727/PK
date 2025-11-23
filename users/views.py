from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile
from patients.models import Patient
from therapy.models import Therapist  # using the Therapist model from therapy app


# ----------------- BASIC PAGES ----------------- #

def landing_page(request):
    return render(request, "landing.html")


def auth_page(request):
    # This is your big login/signup UI (login.html)
    return render(request, "login.html")


# ----------------- SIGNUP API ----------------- #

@method_decorator(csrf_exempt, name="dispatch")
class SignupAPI(APIView):
    """
    POST /api/auth/signup/

    Expected JSON (from login.html):
    {
        "role": "patient" | "therapist",
        "full_name": "...",
        "email": "...",
        "password": "...",
        "dob": "YYYY-MM-DD",
        "gender": "...",        # patient
        "address": "...",       # patient
        "allergies": "...",     # patient
        "experience": "3",      # therapist
        "license_no": "...",    # therapist (not stored exactly, but we still accept it)
        "qualification": "...", # therapist
        "expertise": ["Vamana", "Nasya", ...]  # therapist
    }
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        role = data.get("role")
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")

        if not role or not full_name or not email or not password:
            return Response(
                {"error": "role, full_name, email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if role not in ["patient", "therapist", "admin"]:
            return Response(
                {"error": "Invalid role."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "This email is already registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create username from email, ensure unique
        base_username = email.split("@")[0]
        username = base_username
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        # create Django user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # create profile
        UserProfile.objects.create(
            user=user,
            role=role,
            full_name=full_name,
        )

        # create patient / therapist records
        if role == "patient":
            Patient.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                gender=data.get("gender", ""),
                address=data.get("address", ""),
                allergies=data.get("allergies", ""),
                date_of_birth=data.get("dob") or None,
            )

        elif role == "therapist":
            # expertise list -> string
            expertise = data.get("expertise", [])
            if isinstance(expertise, list):
                expertise = ", ".join(expertise)

            Therapist.objects.create(
                full_name=full_name,
                email=email,
                specialization=expertise or data.get("qualification", ""),
                experience_years=int(data.get("experience") or 0),
                phone="",  # not collected in form
            )

        # admin role: only User + UserProfile for now

        return Response(
            {"message": "Signup successful", "role": role},
            status=status.HTTP_201_CREATED,
        )


# ----------------- LOGIN API ----------------- #

@method_decorator(csrf_exempt, name="dispatch")
class LoginAPI(APIView):
    """
    POST /api/auth/login/
    { "email": "...", "password": "..." }

    Response:
    { "message": "Login successful", "role": "patient|therapist|admin" }
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request,
            username=user_obj.username,
            password=password,
        )

        if user is None:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # login the user into Django session
        login(request, user)

        try:
            role = user.profile.role
        except UserProfile.DoesNotExist:
            role = "patient"

        return Response(
            {"message": "Login successful", "role": role},
            status=status.HTTP_200_OK,
        )


# ----------------- DASHBOARD VIEWS ----------------- #

@login_required
def patient_dashboard(request):
    # template already exists: templates/patient_portal/dashboard.html
    return render(request, "patient_portal/dashboard.html")


@login_required
def therapist_dashboard(request):
    # template: templates/therapist-portel/therapist.html
    return render(request, "therapist-portel/therapist.html")


@login_required
def admin_dashboard(request):
    # template: templates/admin_portal/admin_dashboard.html
    return render(request, "admin_portal/admin_dashboard.html")
