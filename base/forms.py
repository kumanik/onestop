from typing import Tuple
from django.forms import ModelForm
from .models import *


class EventForm(ModelForm):
    model = Event
    exclude = ('student_lists', 'name', )


class FileForm(ModelForm):
    model = File
    exclude = ()


class StudentListForm(ModelForm):
    model = StudentList
    exclude = ('list', )


class Student(ModelForm):
    model = Student
    exclude = ()


class SinglelineForm(ModelForm):
    model = SingleLine
    exclude = ()
