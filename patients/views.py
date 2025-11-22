from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, date

from .models import Therapy, Therapist, PatientAppointment, TherapistAppointment


# ============================
# BILLING PAGE
# ============================


# ============================
# PROFILE PAGE
# ============================
def profile(request):
    return render(request, 'patient_portal/profile.html')


# ============================
# APPOINTMENTS PAGE
# ============================
def appointments(request):

    therapies = Therapy.objects.all()
    therapists = Therapist.objects.all()

    patient_name = "Aniket"   # later: request.user.name

    # upcoming appointments
    upcoming = PatientAppointment.objects.filter(
        patient_name=patient_name,
        date__gte=date.today()
    ).order_by('date', 'time')

    # old appointments
    history = PatientAppointment.objects.filter(
        patient_name=patient_name,
        date__lt=date.today()
    ).order_by('-date')


    # BOOKING PROCESS
    if request.method == 'POST':
        therapy_id = request.POST.get('therapy')
        therapist_id = request.POST.get('therapist')
        appt_date = request.POST.get('date')
        appt_time = request.POST.get('time')

        therapy = get_object_or_404(Therapy, id=therapy_id)
        therapist = get_object_or_404(Therapist, id=therapist_id)

        # save in patient table
        PatientAppointment.objects.create(
            patient_name=patient_name,
            therapy=therapy,
            therapist=therapist,
            date=appt_date,
            time=appt_time
        )

        # mirror save in therapist table
        TherapistAppointment.objects.create(
            therapist=therapist,
            patient_name=patient_name,
            therapy=therapy,
            date=appt_date,
            time=appt_time
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('appointments')

    return render(request, 'patient_portal/appointments.html', {
        "therapies": therapies,
        "therapists": therapists,
        "upcoming": upcoming,
        "history": history
    })


# ============================
# CANCEL APPOINTMENT
# ============================
def cancel_appointment(request, appt_id):

    appt = get_object_or_404(PatientAppointment, id=appt_id)

    # delete mirror record
    TherapistAppointment.objects.filter(
        therapist=appt.therapist,
        patient_name=appt.patient_name,
        date=appt.date,
        time=appt.time
    ).delete()

    appt.delete()
    messages.success(request, "Appointment cancelled.")
    return redirect('appointments')


# ============================
# AVAILABLE SLOTS API
# ============================
def slots_api(request):
    appt_date = request.GET.get("date")
    therapist_id = request.GET.get("therapist")

    if not appt_date:
        return JsonResponse({"slots": []})

    all_slots = ["09:00 AM", "10:30 AM", "01:00 PM", "03:30 PM", "05:00 PM"]

    booked = PatientAppointment.objects.filter(
        therapist_id=therapist_id,
        date=appt_date
    )

    booked_times = {
        b.time.strftime("%I:%M %p") for b in booked
    }

    available = [slot for slot in all_slots if slot not in booked_times]

    return JsonResponse({"slots": available})


# ============================
# PATIENT DASHBOARD
# ============================
def dashboard(request):
    patient_name = request.user.get_full_name() if request.user.is_authenticated else "Aniket"

    today = date.today()

    appts = PatientAppointment.objects.filter(
        patient_name=patient_name
    ).order_by('date', 'time')

    # MULTIPLE appointments (QuerySet)
    upcoming = appts.filter(date__gte=today).order_by('date', 'time')

    previous = appts.filter(date__lt=today).order_by('-date', '-time')[:5]

    return render(request, 'patient_portal/dashboard.html', {
        "upcoming": upcoming,
        "previous": previous,
    })


from .models import Billing

# ============================
# BILLING PAGE  (FINAL)
# ============================
from .models import Billing

def billing(request):
    patient_name = "Aniket"  # Later replace with request.user

    pending = Billing.objects.filter(
        patient_name=patient_name,
        status="Pending"
    )

    history = Billing.objects.filter(
        patient_name=patient_name,
        status="Paid"
    )

    return render(request, 'patient_portal/billing.html', {
        "pending": pending,
        "history": history
    })

from .models import Billing

def mark_paid(request, invoice_id):
    bill = get_object_or_404(Billing, invoice_id=invoice_id)
    bill.status = "Paid"
    bill.save()

    messages.success(request, "Bill marked as paid!")
    return redirect("billing")


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import UserProfile
from patients.models import Patient  # 👈 IMPORTANT: add this


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

        # extra fields
        dob = data.get("dob")
        gender = data.get("gender")
        address = data.get("address")
        allergies = data.get("allergies")

        if not email or not password or not full_name:
            return Response({"error": "Required fields missing"}, status=400)

        if User.objects.filter(username=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        # create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        # create user profile
        profile = UserProfile.objects.create(
            user=user,
            full_name=full_name,
            role=role
        )

        # only if patient → save details in Patient table
        if role == "patient":
            Patient.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                gender=gender,
                address=address,
                allergies=allergies,
                date_of_birth=dob
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
from patients.models import Patient
