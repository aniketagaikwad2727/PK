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
    authentication_classes = []   # 🔥 CSRF Disabled for API
    permission_classes = []       # 🔥 Allow all

    def post(self, request):
        data = request.data

        name = data.get("full_name") or ""
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "patient")

        if not email or not password:
            return Response({"error": "Email & Password required"}, status=400)

        if User.objects.filter(username=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        UserProfile.objects.create(
            user=user,
            full_name=name,
            role=role,
        )

        return Response({"message": "Account created successfully"}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        email = data.get("email")
        password = data.get("password")

        print("=== LOGIN DEBUG ===")
        print("Email:", email)
        print("Password:", password)

        # 🔥 Step 1: User ko manually fetch karo
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

        # 🔥 Step 2: Password manually check karo
        if not user.check_password(password):
            print("❌ Password mismatch")
            return Response({"error": "Invalid password"}, status=400)

        print("✅ Password matched")

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
