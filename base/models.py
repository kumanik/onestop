from mongoengine import *


class Student(DynamicDocument):
    name = StringField(max_length=256)
    meta = {'db_alias': 'default'}

    def __lt__(self, other):
        return self.name < other.name


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
    student_lists = ListField(ReferenceField(StudentList))
    meta = {'db_alias': 'default'}

    def delete(self, *args, **kwargs):
        for list in self.student_lists:
            list.delete()
        super(Event, self).delete(*args, **kwargs)


class File(Document):
    file = FileField()
    input = StringField(max_length=256)
    meta = {'db_alias': 'default'}
