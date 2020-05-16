from django.shortcuts import render, redirect, get_object_or_404
from .models import *


def listEvents(request):
    list_events = Event.objects.order_by['name']
    return render(request, "", list_events )


def listStudents(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    student_lists = event.student_lists
    return render(request, '', student_lists )