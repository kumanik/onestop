from mongoengine import *
from decouple import config


class Student(DynamicDocument):
    name = StringField(max_length=256)
    meta = {'db_alias': 'default'}


class StudentList(DynamicDocument):
    type = StringField(max_length=256)
    list = ListField(ReferenceField(Student, reverse_delete_rule=PULL))
    meta = {'db_alias': 'default'}

    def delete(self, *args, **kwargs):
        for student in self.list:
            student.delete()
        super(StudentList, self).delete(*args, **kwargs)


class Event(DynamicDocument):
    name = StringField(max_length=256)
    student_lists = ListField(ReferenceField(StudentList, reverse_delete_rule=PULL))
    meta = {'db_alias': 'default'}


class File(Document):
    file = FileField()
    input = StringField(max_length=256)
    meta = {'db_alias': 'default'}
