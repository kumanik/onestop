from typing import Tuple
from mongodbforms import DocumentForm
from .models import File


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
