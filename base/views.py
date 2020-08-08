from django.shortcuts import render, redirect
from .models import Event, StudentList, Student
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
from django.http import JsonResponse, HttpResponse
import operator
from django.conf import settings


def listEvents(request):
    events = Event.objects.all()
    return render(request, "base/eventList.html", {"events": events})


def search(request):
    query = request.GET.get('search')
    events = Event.objects.filter(name__icontains=query)
    return render(request, 'base/eventList.html', {'events': events})


def search_field(request):
    query = request.GET.get('search_field')
    querys = request.GET.get('searches')
    query = query.upper()
    studentList_ids = []
    if querys.isnumeric():
        field = query
    else:
        field = query+"__icontains"
    val = querys
    students = Student.objects.filter(**{field: val})
    for stu in students:
        stu_list = StudentList.objects.get(list__contains=stu.id)
        studentList_ids.append(stu_list.id)
    events = Event.objects.filter(student_lists__in=studentList_ids)
    return render(request, 'base/studentSearch.html', {'events': events, 'student_event': students})


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
    context = {
        'event': event,
        'event_dict': event_dict,
        'count': count,
        'eventss': eventss
    }
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
    context = {
        'event': event,
        'event_dict': event_dict,
        'count': count,
        'eventss': eventss
    }
    return render(request, 'base/eventDetails.html', context)


def create_event(request):
    if request.POST.get("action") == "post":
        data = json.loads(request.POST.get("json_sent"))
        event = Event(**data)
        event.save()
        return redirect("index")
    return render(request, "base/addEvent.html")


def deleteEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect("index")


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
        request,
        "base/updateEvent.html",
        {"event": event, "event_dict": event_dict}
    )


def sort_by(list_id, sort_by):
    student_list = StudentList.objects.get(id=list_id)
    try:
        if sort_by[0] == '-':
            student_list.list = sorted(
                student_list.list,
                key=lambda mbr:
                    (int(operator.attrgetter(sort_by[1:])(mbr) or 0)),
                reverse=True
            )
        else:
            if sort_by[0] == '+':
                sort_by = sort_by[1:]
            student_list.list = sorted(
                student_list.list,
                key=lambda mbr:
                    (int(operator.attrgetter(sort_by)(mbr) or 0)),
                reverse=False
            )
    except ValueError:
        if sort_by[0] == '-':
            student_list.list = sorted(
                student_list.list,
                key=lambda mbr:
                    (operator.attrgetter(sort_by[1:])(mbr) or " ").lower(),
                reverse=True
            )
        else:
            if sort_by[0] == '+':
                sort_by = sort_by[1:]
            student_list.list = sorted(
                student_list.list,
                key=lambda mbr:
                    (operator.attrgetter(sort_by)(mbr) or " ").lower(),
                reverse=False
            )
    return student_list


def viewStudentList(request, list_id):
    student_list = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__contains=student_list.id)
    order_by = request.GET.get('order_by', None)
    if order_by is not None:
        student_list = sort_by(list_id, order_by)
    return render(
        request,
        "base/studentList.html",
        {"student_list": student_list, "event": event}
    )


def deleteStudentList(request, list_id):
    list1 = StudentList.objects.get(id=list_id)
    event = Event.objects.get(student_lists__contains=list1.id)
    list1.delete()
    return redirect("viewEvent", event.id)


def merge_file(request, list_id):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES.get('file'))
        data = request.FILES.get('file')
        list1 = StudentList.objects.get(id=list_id)
        previous = []
        c = 0
        for lists in list1.list:
            student_dict = lists.to_mongo().to_dict()
            student_dict.pop('_id')
            previous.append(student_dict)
        with open('base/upload/' + data.name, 'r') as csv_file:
            datas = csv.DictReader(csv_file)
            keys_new = datas.fieldnames
            keys_init = [k for k, v in previous[0].items()]
            if len(keys_new) == len(keys_init):
                for k in keys_init:
                    if k not in keys_new:
                        return JsonResponse(
                            {"error": "Fields on original and new data do not match"},
                            status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(
                    {"error": "Fields on original and new data do not match"},
                    status=status.HTTP_400_BAD_REQUEST)
            for row in datas:
                c = 0
                for student in previous:
                    if row == student:
                        c = 1
                if c == 0:
                    stu = Student(**row)
                    stu.save()
                    list1.list.append(stu)
        os.remove('base/upload/' + data.name)
        list1.save()
        return redirect('viewStudents', list_id)


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
    with open('base/upload/' + f.name, 'r') as check:
        seen = check.readlines()
    seen[0] = seen[0].upper()
    with open('base/upload/' + f.name, 'w') as check:
        check.writelines(seen)


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
                    row = {k: v or None for k, v in row.items()}
                    stu = Student(**row)
                    stu.save()
                    list1.list.append(stu)
            os.remove("base/upload/" + data.name)
        list1.save()
        event.student_lists.append(list1)
        event.save()
        return redirect("viewEvent", event_id)


def updateStudent(request, student_id):
    stu = Student.objects.get(id=student_id)
    list = StudentList.objects.filter(list__contains=stu.id)[0]
    stu1st = list.list[0]
    event = Event.objects.filter(student_lists__contains=list.id)
    stu_dict = stu.to_mongo().to_dict()
    stu_dict.pop("_id")
    keys = []
    keys_to_add = []
    for key, val in stu1st.to_mongo().to_dict().items():
        keys.append(key)
    if request.POST.get("action") == "post":
        data = json.loads(request.POST.get("json_sent"))
        for key, value in data.items():
            stu.update(**{key: value})
            if key not in keys:
                keys_to_add.append(key)
        addField(list.id, keys_to_add)
        stu.save()
        return redirect("viewStudents", list.id)
    return render(request, "base/updateStudent.html", {
        "stu": stu, "stu_dict": stu_dict, "event": event, "stulist": list
    })


def createStudent(request, list_id):
    list = StudentList.objects.get(id=list_id)
    try:
        stu1st = list.list[0].to_mongo().to_dict()
        stu1st.pop('_id')
    except AttributeError or KeyError:
        stu1st = None
    if request.POST.get("action") == "post":
        data = json.loads(request.POST.get("json_sent"))
        stu = Student(**data)
        stu.save()
        if stu1st is not None:
            keys = []
            keys_to_add = []
            for key, val in stu1st.items():
                keys.append(key)
            for key, value in data.items():
                if key not in keys:
                    keys_to_add.append(key)
            addField(list.id, keys_to_add)
        list.list.append(stu)
        list.save()
        return render(
            request,
            "base/addStudent.html",
            {'list': list, 'stu1st': stu1st}
        )
    return render(
        request,
        "base/addStudent.html",
        {'list': list, 'stu1st': stu1st}
    )


def addField(list_id, keys):
    list = StudentList.objects.get(id=list_id)
    for each in list.list:
        for key in keys:
            each.update(**{key: None})
        each.save()
    return None


def deleteStudent(request, student_id):
    stu = Student.objects.get(id=student_id)
    list = StudentList.objects.filter(list__contains=stu.id)[0]
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
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            print(serializer.errors)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                "INVALID API KEY",
                status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(
            "API KEY NOT PROVIDED",
            status=status.HTTP_401_UNAUTHORIZED
        )


def handler404(request, exception):
    return render(request, 'base/404.html', status=404)


def handler500(request):
    return render(request, 'base/500.html', status=500)
