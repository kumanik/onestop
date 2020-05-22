from typing import Tuple
from mongodbforms import DocumentForm
from .models import *



class EventForm(DocumentForm):
    class Meta:
        model = Event
        exclude = ('student_lists', 'name', )


class FileForm(DocumentForm):
    class Meta:
        document = File
        exclude = ()


class StudentListForm(DocumentForm):
    class Meta:
        model = StudentList
        exclude = ('list', )


class Student(DocumentForm):
    class Meta:
        model = Student
        exclude = ()


class SinglelineForm(DocumentForm):
    class Meta:
        model = SingleLine
        exclude = ()
