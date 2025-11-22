from django.contrib import admin
from django.urls import include, path
from users.views import auth_page, landing_page

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', landing_page, name='landing'),

    path('login/', auth_page, name='auth-page'),

    # FIXED: API ROUTES
    path('api/auth/', include('users.urls')),

    path('sessions/', include('user_sessions.urls')),
    path('patient/', include('patients.urls')),
]
