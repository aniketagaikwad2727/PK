from django.urls import path
from .views import TherapySessionCreateView, session_list_page, MySessionsAPI

urlpatterns = [
    path("create/", TherapySessionCreateView.as_view()),
    path("list/", session_list_page),
    path("api/my-sessions/", MySessionsAPI.as_view()),
]
