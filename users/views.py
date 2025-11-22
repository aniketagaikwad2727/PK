from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import BasicAuthentication

from .models import UserProfile


def auth_page(request):
    return render(request, 'login.html')


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

        if not full_name or not email or not password:
            return Response({"error": "Missing required fields"}, status=400)

        if User.objects.filter(username=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        # Create Django user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            role=role,
        )

        # =============================
        # STORE PATIENT DATA
        # =============================
        if role == "patient":
            Patient.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                date_of_birth=data.get("dob"),
                gender=data.get("gender"),
                address=data.get("address"),
                allergies=data.get("allergies"),
            )

        # =============================
        # STORE THERAPIST DATA
        # =============================
        elif role == "therapist":
            Therapist.objects.create(
                user=user,
                name=full_name,
                email=email,
                dob=data.get("dob"),
                experience=data.get("experience"),
                license_no=data.get("license_no"),
                qualification=data.get("qualification"),
                expertise=",".join(data.get("expertise", [])),
            )

        return Response({"message": "Account created successfully!"}, status=201)


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

        return Response({"message": "Login successful", "role": role})



from django.contrib.auth.decorators import login_required

@login_required
def patient_dashboard(request):
    return render(request, "patient_portal/patient-dashboard.html")
    
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')
