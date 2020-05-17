from django.shortcuts import render, redirect, get_object_or_404
from .models import *


def listEvents(request):
    events = Event.objects.order_by['name']
    return render(request, "base/eventList.html", {'events': events})


def viewEvent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    student_lists = event.student_lists
    return render(request, '', {'student_lists': student_lists, 'event': event})


def viewStudentList(request, student_list_id):
    student_list = get_object_or_404(StudentList, id=student_list_id)
    return render(request, "base/studentList.html", {'student_list': student_list})


