from mongoengine import *


class Event(DynamicEmbeddedDocument):
    single_input = DictField()


class Student(DynamicEmbeddedDocument):
    single_input = DictField()


class StudentList(DynamicDocument):
    event = EmbeddedDocumentField(Event)
    type = StringField(max_length=256)
    list = ListField(EmbeddedDocumentField(Student))


class File(Document):
    file = FileField()