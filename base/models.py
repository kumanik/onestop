# from django.db import models
from mongoengine import *


class Event(DynamicEmbeddedDocument):
    name = StringField(max_length=256)
    single_input = DictField()


class Student(DynamicEmbeddedDocument):
    name = StringField(max_length=256)


class StudentList(DynamicDocument):
    event = EmbeddedDocumentField(Event)
    type = StringField(max_length=256)
    list = ListField(EmbeddedDocumentField(Student))


class File(Document):
    file = FileField()
