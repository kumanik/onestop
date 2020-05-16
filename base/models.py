from mongoengine import *


class Student(DynamicEmbeddedDocument):
    name = StringField(max_length=256)
    single_input = DictField()


class StudentList(DynamicEmbeddedDocument):
    type = StringField(max_length=256)
    list = ListField(EmbeddedDocumentField(Student))


class Event(DynamicDocument):
    name = StringField(max_length=256)
    single_input = DictField()
    student_lists = ListField(StudentList)


class File(Document):
    file = FileField()
