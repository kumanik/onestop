from typing import Tuple
from mongodbforms import DocumentForm, documentformset_factory
from .models import *


# class EventForm(DocumentForm):
#     class Meta:
#         model = Event
#         exclude = ('student_lists', 'name', )


# class StudentListForm(DocumentForm):
#     class Meta:
#         model = StudentList
#         exclude = ('list', )


# class Student(DocumentForm):
#     class Meta:
#         model = Student
#         exclude = ()


class FileForm(DocumentForm):
    class Meta:
        document = File
        fields = [
            'file', 'input',
        ]


class SingleLineForm(DocumentForm):
    class Meta:
        document = SingleLine
        fields = [
            'field_name', 'field_value',
        ]

