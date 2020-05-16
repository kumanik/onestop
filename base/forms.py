from django import forms
from django.forms import ModelForm, Textarea
from .models import *


class EventForm(ModelForm):
    model = Event
    exclude = ()
    widgets = {
        'single_input': Textarea(attrs={'rows': 10}),
    }


class FileForm(ModelForm):
    model = File
    exclude = ()


class StudentListForm(ModelForm):
    model = StudentList
    exclude = ('list','event',)


class Student(ModelForm):
    model = Student
    exclude = ()
    widgets = {
        'single_input': Textarea(attrs={'rows': 10}),
    }
