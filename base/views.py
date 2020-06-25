from django.shortcuts import render, redirect
from .models import Event, StudentList, Student
from .forms import FileForm
import csv
import os
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from .serializers import EventSerializer
import json
from rest_framework.decorators import api_view
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import api_key
from django.http import JsonResponse
import operator


@staff_member_required(login_url="/accounts/login/")
def listEvents(request):
    events = Event.objects.all()
    return render(request, "base/eventList.html", {"events": events})


def search(request):
    query = request.GET.get('search')
    events = Event.objects.filter(name__icontains=query)
    return render(request, 'base/eventList.html', {'events': events})


def search_name(request):
    query = request.GET.get('search_name')
    studs = Student.objects.filter(name__icontains=query)
    abc = []
    stuid = []
    for i in studs:
        r = StudentList.objects.get(list__contains=i.id)
        stuid.append(i.id)
        abc.append(r.id)
    student_event = Student.objects.filter(id__in=stuid)
    t = Event.objects.filter(student_lists__in=abc)
    return render(request, 'base/studentSearch.html', {'events': t, 'student_event': student_event})


@staff_member_required
def viewEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    event_dict = event.to_mongo().to_dict()
    try:
        event_dict.pop('_id')
        event_dict.pop('student_lists')
        event_dict.pop('name')
    except KeyError:
        pass
    eventss = event.student_lists
    count = len(event.student_lists)
    context = {'event': event, 'event_dict': event_dict, 'count': count, 'eventss': eventss}
    return render(request, 'base/eventDetails.html', context)


def search1(request, event_id):
    query = request.GET.get("search1")
    event = Event.objects.get(id=event_id)
    event_dict = event.to_mongo().to_dict()
    try:
        event_dict.pop('_id')
        event_dict.pop('student_lists')
        event_dict.pop('name')
    except KeyError:
        pass
    eventss = StudentList.objects.filter(type__icontains=query)
    count = len(eventss)
    context = {'event': event, 'event_dict': event_dict, 'count': count, 'eventss': eventss}
    return render(request, 'base/eventDetails.html', context)


@staff_member_required
def create_event(request):
    if request.POST.get("action") == "post":
        data = json.loads(request.POST.get("json_sent"))
        event = Event(**data)
        event.save()
        return redirect("index")
    return render(request, "base/addEvent.html")


@staff_member_required
def deleteEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect("index")


@staff_member_required
def updateEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    event_dict = event.to_mongo().to_dict()
    event_dict.pop("_id")
    event_dict.pop("student_lists")
    if request.POST.get("action") == "post":
        data = json.loads(request.POST.get("json_sent"))
        for key, value in data.items():
            setattr(event, key, value)
        event.save()
        return redirect("viewEvent", event.id)
    return render(
        request, "base/updateEvent.html", {"event": event, "event_dict": event_dict}
    )


@staff_member_required
def viewStudentList(request, list_id):
    student_list = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__contains=student_list.id)
    return render(
        request, "base/studentList.html", {"student_list": student_list, "event": event}
    )


@staff_member_required
def sort_by(request, list_id):
    student_list = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__contains=student_list.id)
    sort_by = request.GET.get('sort_by')
    try:
        if sort_by[0] == '-':
            student_list.list = sorted(student_list.list, key=operator.attrgetter(sort_by[1:]).lower, reverse=True)
        else:
            student_list.list = sorted(student_list.list, key=operator.attrgetter(sort_by).lower, reverse=False)
    except:
        print(sort_by)
        return render(
            request, "base/studentList.html",
            {
                "student_list": student_list,
                "event": event,
                "message": "Enter an attribute present on all objects"
            }
        )
    return render(
        request, "base/studentList.html", {"student_list": student_list, "event": event, "message": None}
    )


@staff_member_required
def deleteStudentList(request, list_id):
    list1 = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__contains=list1.id)
    list1.delete()
    return redirect("viewEvent", event.id)


def handle_uploaded_file(f):
    with open("base/upload/" + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if f.name.endswith(".xlsx"):
        data_xls = pd.read_excel("base/upload/" + f.name)
        data_xls.to_csv("base/upload/" + f.name, encoding="utf-8", index=False)
    df = pd.read_csv("base/upload/" + f.name)
    df.drop_duplicates(inplace=True)
    df.to_csv("base/upload/" + f.name, index=False)


@staff_member_required
def addStudentList(request, event_id):
    if request.method == "POST":
        data = request.FILES.get("file")
        type1 = request.POST.get("input")
        list1 = StudentList(type=type1)
        event = Event.objects.get(id=event_id)
        if data is not None:
            handle_uploaded_file(request.FILES["file"])
            with open("base/upload/" + data.name, "r") as csv_file:
                datas = csv.DictReader(csv_file)
                for row in datas:
                    stu = Student(**row)
                    stu.save()
                    list1.list.append(stu)
            os.remove("base/upload/" + data.name)
        list1.save()
        event.student_lists.append(list1)
        event.save()
        return redirect("viewEvent", event_id)
    else:
        form = FileForm()
    return render(request, "base/upload_file.html", {'form': form})


@staff_member_required
def updateStudent(request, student_id):
    stu = Student.objects.get(id=student_id)
    list = StudentList.objects.filter(list__contains=stu.id)[0]
    event = Event.objects.filter(student_lists__contains=list.id)
    stu_dict = stu.to_mongo().to_dict()
    stu_dict.pop("_id")
    if request.POST.get("action") == "post":
        data = json.loads(request.POST.get("json_sent"))
        for key, value in data.items():
            setattr(stu, key, value)
        stu.save()
        return redirect("viewStudents", list.id)
    return render(request, "base/updateStudent.html", {
        "stu": stu, "stu_dict": stu_dict, "event": event, "stulist": list
    })


@staff_member_required
def createStudent(request, list_id):
    list = StudentList.objects.get(id=list_id)
    try:
        stu1st = list.list[0].to_mongo().to_dict()
        stu1st.pop('_id')
    except:
        stu1st = None
    if request.POST.get("action") == "post":
        data = json.loads(request.POST.get("json_sent"))
        stu = Student(**data)
        stu.save()
        list.list.append(stu)
        list.save()
        return render(request, "base/addStudent.html", {'list': list, 'stu1st': stu1st})
    return render(request, "base/addStudent.html", {'list': list, 'stu1st': stu1st})


@staff_member_required
def deleteStudent(request, student_id):
    stu = Student.objects.get(id=student_id)
    list = StudentList.objects.get(list__contains=stu.id)
    stu.delete()
    return redirect("viewStudents", list.id)


@api_view(['POST'])
def event_APIView(request):
    apikey = request.META.get('HTTP_KEY')
    if apikey is not None:
        if api_key.objects.filter(apiKey=apikey).count() == 1:
            data = request.data
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("INVALID API KEY", status=status.HTTP_403_FORBIDDEN)
    else:
        return Response("API KEY NOT PROVIDED", status=status.HTTP_401_UNAUTHORIZED)


def key_viewer(request):
    key = api_key.objects.get(user=request.user)
    if key is not None:
        return JsonResponse({'key': key.apiKey})
