from . import views
from django.urls import path, include

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('check_staff/', views.check_staff, name='check_staff')
]
