from django.contrib import admin
from django.urls import include, path
from users.views import auth_page   # 👈 add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sessions/', include('user_sessions.urls')),

    # 👇 API for login/signup
    path('api/auth/', include('users.urls')),

    # 👇 Root URL -> login page
    path('', auth_page),
    path('', include('patients.urls')),   # patient dashboard

]
