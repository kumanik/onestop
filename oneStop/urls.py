from django.contrib import admin
from django.urls import path, include
import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('base.urls')),
]

handler404 = base.views.handler404
handler500 = base.views.handler500
