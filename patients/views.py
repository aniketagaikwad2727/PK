from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime

from .models import Therapy, Therapist, PatientAppointment, TherapistAppointment


# def dashboard(request):
#     return render(request, 'patient_portal/dashboard.html')


def billing(request):
    return render(request, 'patient_portal/billing.html')


def profile(request):
    return render(request, 'patient_portal/profile.html')


# ================================
#     APPOINTMENTS MAIN VIEW
# ================================
def appointments(request):
    therapies = Therapy.objects.all()
    therapists = Therapist.objects.all()

    patient_name = "Aniket"   # Later replace with request.user when login done

    # upcoming & history
    upcoming = PatientAppointment.objects.filter(
        patient_name=patient_name
    ).order_by('date', 'time')

    history = PatientAppointment.objects.filter(
        patient_name=patient_name,
        date__lt=datetime.today()
    ).order_by('-date')

    if request.method == 'POST':
        therapy_id = request.POST.get('therapy')
        therapist_id = request.POST.get('therapist')
        date = request.POST.get('date')
        time = request.POST.get('time')

        therapy = get_object_or_404(Therapy, id=therapy_id)
        therapist = get_object_or_404(Therapist, id=therapist_id)

        # Save in patient table
        patient_obj = PatientAppointment.objects.create(
            patient_name=patient_name,
            therapy=therapy,
            therapist=therapist,
            date=date,
            time=time
        )

        # Mirror save in therapist table
        TherapistAppointment.objects.create(
            therapist=therapist,
            patient_name=patient_name,
            therapy=therapy,
            date=date,
            time=time
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('appointments')

    return render(request, 'patient_portal/appointments.html', {
        "therapies": therapies,
        "therapists": therapists,
        "upcoming": upcoming,
        "history": history
    })


# ================================
#     CANCEL APPOINTMENT
# ================================
def cancel_appointment(request, appt_id):
    appt = get_object_or_404(PatientAppointment, id=appt_id)

    # Delete Therapist copy too
    TherapistAppointment.objects.filter(
        therapist=appt.therapist,
        patient_name=appt.patient_name,
        date=appt.date,
        time=appt.time
    ).delete()

    appt.delete()

    messages.success(request, "Appointment cancelled.")
    return redirect('appointments')


# ================================
#     AVAILABLE SLOTS API
# ================================
def slots_api(request):
    date = request.GET.get("date")
    therapist_id = request.GET.get("therapist")

    if not date:
        return JsonResponse({"slots": []})

    # Static slot list
    all_slots = ["09:00 AM", "10:30 AM", "01:00 PM", "03:30 PM", "05:00 PM"]

    # Remove booked slots for that therapist
    booked = PatientAppointment.objects.filter(
        therapist_id=therapist_id,
        date=date
    )

    booked_times = {
        b.time.strftime("%I:%M %p") for b in booked
    }

    available = [slot for slot in all_slots if slot not in booked_times]

    return JsonResponse({"slots": available})


from datetime import date
from .models import PatientAppointment

from datetime import date
from .models import PatientAppointment

from datetime import date
from .models import PatientAppointment

def dashboard(request):
    patient_name = request.user.get_full_name() if request.user.is_authenticated else "Aniket"

    today = date.today()

    # All appointments for this patient
    appts = PatientAppointment.objects.filter(patient_name=patient_name).order_by('date', 'time')

    # Next upcoming appointment
    upcoming = appts.filter(date__gte=today).first()

    # Previous appointments (latest 5)
    previous = appts.filter(date__lt=today).order_by('-date', '-time')[:5]

    context = {
        "upcoming": upcoming,
        "previous": previous,
    }
    return render(request, 'patient_portal/dashboard.html', context)
