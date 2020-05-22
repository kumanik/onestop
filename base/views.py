from django.shortcuts import render, redirect
from .models import *
from .forms import FileForm
import csv


def listEvents(request):
    events = Event.objects.all()
    return render(request, "base/eventList.html", {'events': events})


def viewEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'base/eventDetails.html', {'event': event})


def viewStudentList(request, list_id):
    student_list = StudentList.objects.get(id=list_id)
    return render(request, "base/studentList.html", {'student_list': student_list})


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


def upload_file(request):
    document =File
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file']
            decoded_file = data.read().decode('utf-8').splitlines()
            csv_dict_reader = csv.DictReader(decoded_file)
            lists = StudentList()
            eventss = Event()
            for row in csv_dict_reader:
                stu = Student(row)
                stu.save()
                lists.list.append(stu)
                lists.save()
                eventss.student_lists.append(lists)
                eventss.save()
               
            return redirect('upload_file')
    else:
        form = FileForm()        
    
    return render(request, 'upload_file.html', {
        'form': form
        })


        
    

