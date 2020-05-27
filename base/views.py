from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout
import csv
import json
from django.contrib.auth.decorators import login_required


@login_required
def listEvents(request):
    events = Event.objects.all()
    return render(request, "base/eventList.html", {'events': events})


@login_required
def viewEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'base/eventDetails.html', {'event': event})


@login_required
def viewStudentList(request, list_id):
    student_list = StudentList.objects.get(id=list_id)
    return render(request, "base/studentList.html", {'student_list': student_list})


@login_required
def deleteStudentList(request, list_id):
    list1 = StudentList.objects.get(id=list_id)
    list1.delete()
    return redirect('index')


@login_required
def deleteEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    for list1 in event.student_lists:
        deleteStudentList(request, list1.id)
    event.delete()
    return redirect('index')


@login_required
def upload_student_list(request, event_id):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file']
            type1 = request.POST.get['input']
            decoded_file = data.read().decode('utf-8').splitlines()
            csv_dict_reader = csv.DictReader(decoded_file)
            list1 = StudentList(type=type1)
            event = Event.objects.get(id=event_id)
            for row in csv_dict_reader:
                stu = Student(**row)
                if Student.objects(**row).count() == 0:
                    stu.save()
                    list1.list.append(stu)
                else:
                    pass
            list1.save()
            event.student_lists.append(list1)
            event.save()
            return redirect('viewEvent', event_id)
    else:
        form = FileForm()
    return render(request, "base/upload_file.html", {'form': form})


@login_required
def create_event(request):
    if request.POST.get('action') == 'post':
        data = json.loads(request.POST.get('json_sent'))
        event = Event(**data)
        event.save()
        return redirect('index')
    return render(request, 'base/addEvent.html')