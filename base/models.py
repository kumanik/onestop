# from django.db import models
from mongoengine import *


class Event(EmbeddedDocument):
    name = StringField(max_length=256, required=True)


class Student(EmbeddedDocument):
    name = StringField(max_length=256, required=True)


class StudentList(Document):
    event = EmbeddedDocumentField(Event)
    type = StringField(max_length=256, required=True)
    list = EmbeddedDocumentListField(Student)
