from mongoengine import *


class Student(DynamicEmbeddedDocument):
    name = StringField(max_length=256)


class StudentList(DynamicEmbeddedDocument):
    type = StringField(max_length=256)
    list = ListField(EmbeddedDocumentField(Student))


class Event(DynamicDocument):
    name = StringField(max_length=256)
    student_lists = ListField(StudentList)
    # def get_fields(self):
    #     return [(field.name, field.value_to_string(self)) for field in Event._meta.fields]


class File(Document):
    file = FileField()


class SingleLine(Document):
    single_input = DictField()
