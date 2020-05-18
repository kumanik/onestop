from mongoengine import *


class Student(DynamicDocument):
    name = StringField(max_length=256)


class StudentList(DynamicDocument):
    type = StringField(max_length=256)
    list = ListField(ReferenceField(Student, reverse_delete_rule=CASCADE))


class Event(DynamicDocument):
    name = StringField(max_length=256)
    student_lists = ListField(ReferenceField(StudentList, reverse_delete_rule=CASCADE))


class File(Document):
    file = FileField()


class SingleLine(Document):
    single_input = DictField()
