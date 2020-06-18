from django.urls import path
from base import views

urlpatterns = [
    path("", views.listEvents, name="index"),
    path("newList/", views.search, name="search"),
    path("search_identifier/event/<event_id>", views.search1, name="search1"),
    path("addEvent", views.create_event, name="addEvent"),
    path("event/<event_id>", views.viewEvent, name="viewEvent"),
    path("event/studentlist/<list_id>", views.viewStudentList, name="viewStudents"),
    path("event/delete/<event_id>", views.deleteEvent, name="deleteEvent"),
    path("event/update/<event_id>", views.updateEvent, name="updateEvent"),
    path("event/student_list/delete/<list_id>", views.deleteStudentList, name="deleteStudentList",),
    path("event/addstudentlist/upload/<event_id>", views.upload_student_list, name="upload_studentlist",),
]
