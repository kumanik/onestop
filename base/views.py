from django.shortcuts import render, redirect
from .models import *


def listEvents(request):
    events = Event.objects.all()
    return render(request, "base/eventList.html", {'events': events})


def viewEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'base/eventDetails.html', {'event': event})


def viewStudentList(request, list_id):
    student_list = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__=student_list)
    return render(request, "base/studentList.html", {'student_list': student_list, 'event': event})


def deleteStudentList(request, list_id):
    list1 = StudentList.objects.get(id=list_id)
    list1.delete()
    return redirect('index')


def deleteEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    for list1 in event.student_lists:
        deleteStudentList(request, list1.id)
    event.delete()
    return redirect('index')



