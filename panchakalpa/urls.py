from django.contrib import admin
from django.urls import include, path
from users.views import auth_page, landing_page

urlpatterns = [
    path('admin/', admin.site.urls),

    # Landing page (HOME PAGE)
    path('', landing_page, name='landing'),

    # Login page
    path('login/', auth_page, name='auth-page'),

    # User Auth API
    path('api/auth/', include('users.urls')),

    # User Sessions API
    path('sessions/', include('user_sessions.urls')),

    # Patient dashboard
    path('patient/', include('patients.urls')),
    path('panchkalpa/', include('patients.urls')),

]
