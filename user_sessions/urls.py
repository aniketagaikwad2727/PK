from django.urls import path
from .views import TherapySessionCreateView, session_list_page, MySessionsAPI

urlpatterns = [
    # Create a therapy session (API)
    path("create/", TherapySessionCreateView.as_view(), name="create_session"),

    # List all sessions (HTML page)
    path("list/", session_list_page, name="session_list_page"),

    # Session list API for dashboard
    path("api/my-sessions/", MySessionsAPI.as_view(), name="my_sessions_api"),
]
