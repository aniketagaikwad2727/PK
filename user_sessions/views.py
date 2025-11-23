from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import TherapySession
from .serializers import TherapySessionSerializer


# =====================================================
# CREATE THERAPY SESSION (API)
# =====================================================
class TherapySessionCreateView(generics.CreateAPIView):
    queryset = TherapySession.objects.all()
    serializer_class = TherapySessionSerializer


# =====================================================
# SESSION LIST PAGE (HTML PAGE)
# =====================================================
def session_list_page(request):
    sessions = TherapySession.objects.all()

    return render(request, "patient_portal/sessions.html", {
        "sessions": sessions
    })


# =====================================================
# SESSION API FOR FRONTEND DASHBOARD
# =====================================================
class MySessionsAPI(APIView):

    def get(self, request):

        sessions = TherapySession.objects.all()

        formatted = []

        for s in sessions:
            formatted.append({
                "date": str(s.session_date),
                "time": f"{s.session_start} - {s.session_end}",
                "therapy": s.therapy.name,
                "status": "Completed",       # static until real workflow added
                "needsFeedback": False,
                "practitioner": s.therapist.full_name if s.therapist else "",
                "room": "Room 203",
            })

        return Response(formatted)
