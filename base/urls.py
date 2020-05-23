from django.urls import path
from .views import *
from base import views

urlpatterns = [
    path("", listEvents, name="index"),
    path("event/<event_id>", viewEvent, name="viewEvent"),
    path("event/studentlist/<list_id>", viewStudentList, name="viewStudents"),
    path("event/delete/<event_id>", deleteEvent, name="deleteEvent"),
    path("event/student_list/delete/<list_id>", deleteStudentList, name="deleteStudentList"),
    path("event/addstudentlist/upload/<event_id>", upload_student_list, name="upload_studentlist"),
]
