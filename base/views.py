from django.shortcuts import render, redirect
from .models import *
from .forms import *
import csv
import os
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
import requests
from requests.exceptions import HTTPError
import json



@login_required
def listEvents(request):
    events = Event.objects.all()
    return render(request, "base/eventList.html", {'events': events})

def search(request):
    query = request.GET.get('search')
    events = Event.objects.filter(name__icontains = query)
    return render(request, 'base/eventList.html', {'events': events})

@login_required
def viewEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    event_dict = event.to_mongo().to_dict()
    try:
        event_dict.pop('_id')
        event_dict.pop('student_lists')
        event_dict.pop('name')
    except:
        pass
    eventss = event.student_lists
    count = len(event.student_lists)
    name = event.name
    url1 = "https://my-json-server.typicode.com/typicode/demo/db"
    response = requests.get(url1)
    if response.text == '':
        print("no data")
    geodata = response.json()
    posts = geodata['posts']
    '''a = 'posts'
    listed = geodata[a]
    list2 = StudentList(type=a)
    for row in listed:
        print(row)
        stud = Student(**row)
        stud.save()
        list2.list.append(stud)
    list2.save()'''
    return render(request, 'base/eventDetails.html', {'event': event, 'event_dict': event_dict, 'count': count, 'eventss': eventss, 'posts': posts})

def search1(request, event_id):
    query = request.GET.get('search1')
    event = Event.objects.get(id=event_id)
    event_dict = event.to_mongo().to_dict()
    try:
        event_dict.pop('_id')
        event_dict.pop('student_lists')
        event_dict.pop('name')
    except:
        pass
    eventss = StudentList.objects.filter(type__icontains=query)
    count = len(eventss)
    return render(request, 'base/eventDetails.html', {'event': event, 'event_dict': event_dict, 'count': count, 'eventss': eventss})



@login_required
def create_event(request):
    if request.POST.get('action') == 'post':
        data = json.loads(request.POST.get('json_sent'))
        event = Event(**data)
        event.save()
        return redirect('index')
    return render(request, 'base/addEvent.html')


@login_required
def deleteEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    for list1 in event.student_lists:
        deleteStudentList(request, list1.id)
    event.delete()
    return redirect('index')


@login_required
def updateEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    event_dict = event.to_mongo().to_dict()
    event_dict.pop('_id')
    event_dict.pop('student_lists')
    if request.POST.get('action') == 'post':
        data = json.loads(request.POST.get('json_sent'))
        print(data)
        for key, value in data.items():
            setattr(event, key, value)
        event.save()
        return redirect('viewEvent', event.id)
    return render(request, 'base/update_event.html', {'event': event, 'event_dict': event_dict})


@login_required
def viewStudentList(request, list_id):
    student_list = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__contains=student_list.id)
    return render(request, "base/studentList.html", {'student_list': student_list, 'event': event})


@login_required
def deleteStudentList(request, list_id):
    list1 = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__contains=list1.id)
    list1.delete()
    return redirect('viewEvent', event.id)


def handle_uploaded_file(f):
    with open('base/upload/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if f.name.endswith('.xlsx'):
        data_xls = pd.read_excel('base/upload/' + f.name)
        data_xls.to_csv('base/upload/' + f.name, encoding='utf-8', index=False)
    df = pd.read_csv('base/upload/' + f.name)
    df.drop_duplicates(inplace=True)
    df.to_csv('base/upload/' + f.name, index=False)


@login_required
def upload_student_list(request, event_id):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'])
        data = request.FILES['file']
        type1 = request.POST.get('input')
        list1 = StudentList(type=type1)
        event = Event.objects.get(id=event_id)
        with open('base/upload/' + data.name, 'r') as csv_file:
            datas = csv.DictReader(csv_file)
            for row in datas:
                stu = Student(**row)
                stu.save()
                list1.list.append(stu)
        os.remove('base/upload/' + data.name)
        list1.save()
        event.student_lists.append(list1)
        event.save()
        return redirect('viewEvent', event_id)
    else:
        form = FileForm()
    return render(request, "base/upload_file.html", {'form': form})



class EventView(APIView):

    def get(self, request):
        serializer = EventSerializer(Event.objects.all(), many=True)
        response = {"base": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            eve = Event(**data)
            eve.save()
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)


class StudentView(APIView):

    def get(self, request):
        serializer = StudentSerializer(Student.objects.all(), many=True)
        response = {"base": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            eve = Student(**data)
            eve.save()
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)






   
