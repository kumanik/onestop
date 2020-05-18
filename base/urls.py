from django.urls import path
from .views import *

urlpatterns = [
    path("", listEvents, name="index"),
    path("event/<int:event_id>", viewEvent, name="viewEvent"),
    path("event/studentlist/<int:list_id>", viewStudentList, name="viewStudents"),
]
