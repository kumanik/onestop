# from django.db import models
from mongoengine import *


def get_event_names():
    event_names = {}
    for event in Event.objects:
        event_names.update({event.name: event.name})
    return event_names


class StudentList(EmbeddedDocument):
    event_name = StringField(choices=get_event_names().keys())
    type = StringField(max_length=256, required=True)
    list = ListField()


class Event(Document):
    name = StringField(max_length=256, required=True)
    students = EmbeddedDocumentField(StudentList)
