from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import TherapySession
from .serializers import TherapySessionSerializer

class TherapySessionCreateView(generics.CreateAPIView):
    queryset = TherapySession.objects.all()
    serializer_class = TherapySessionSerializer


from rest_framework.views import APIView
from rest_framework.response import Response

def session_list_page(request):
    sessions = TherapySession.objects.all()
    return render(request, "patient_portal/sessions.html", {"sessions": sessions})


class MySessionsAPI(APIView):
    def get(self, request):
        sessions = TherapySession.objects.all()

        formatted = []
        for s in sessions:
            formatted.append({
                "date": str(s.date),
                "time": f"{s.start_time} - {s.end_time}",
                "therapy": s.session_type,
                "status": "Completed" if s.is_completed else "Upcoming",
                "needsFeedback": False,
                "practitioner": str(s.therapist),
                "room": "Room 203"
            })

        return Response(formatted)
