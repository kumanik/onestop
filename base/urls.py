from django.urls import path
from django.conf.urls import url
from .views import *
from base import views

urlpatterns = [
    path("", listEvents, name="index"),

    path("newList/", search, name="search"),

    path("search_identifier/event/<event_id>", search1, name="search1"),

    path("addEvent", create_event, name="addEvent"),

    path("event/<event_id>", viewEvent, name="viewEvent"),

    path("event/studentlist/<list_id>", viewStudentList, name="viewStudents"),

    path("event/delete/<event_id>", deleteEvent, name="deleteEvent"),

    path("event/update/<event_id>", updateEvent, name="updateEvent"),

    path("event/student_list/delete/<list_id>", deleteStudentList, name="deleteStudentList"),

    path("event/addstudentlist/upload/<event_id>", upload_student_list, name="upload_studentlist"),

    path("api/", views.EventView.as_view()),

    path("apis/", views.StudentView.as_view()),


]
