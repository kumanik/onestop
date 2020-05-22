from typing import Tuple
from django.forms import ModelForm
from mongodbforms import EmbeddedDocumentForm, DocumentForm
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
