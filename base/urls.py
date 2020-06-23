from django.urls import path
from base import views

urlpatterns = [

    # Search
    path("newList/", views.search, name="search"),
    path("search_identifier/event/<event_id>", views.search1, name="search1"),
    path("searchStudentName/", views.search_name, name="search_name"),

    # Event Model
    path("", views.listEvents, name="index"),
    path("addEvent", views.create_event, name="addEvent"),
    path("event/<event_id>", views.viewEvent, name="viewEvent"),
    path("event/delete/<event_id>", views.deleteEvent, name="deleteEvent"),
    path("event/update/<event_id>", views.updateEvent, name="updateEvent"),

    # StudentList Model
    path("event/studentlist/<list_id>", views.viewStudentList, name="viewStudents"),
    path("event/student_list/delete/<list_id>", views.deleteStudentList, name="deleteStudentList"),
    path("event/addstudentlist/upload/<event_id>", views.upload_student_list, name="upload_studentlist"),

    # Student model
    path("event/studentlist/student/<student_id>", views.updateStudent, name="updateStudent"),
    path("event/studentlist/student/add/<list_id>", views.createStudent, name="addStudent"),
    path("event/studentlist/student/delete/<student_id>", views.deleteStudent, name="deleteStudent"),

    # API
    path("api/event", views.event_APIView),
    path("key", views.key_viewer, name="showKey"),
]
