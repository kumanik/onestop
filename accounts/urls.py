from .views import *
from django.urls import path, include

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
