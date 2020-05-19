from mongoengine import *


class Student(DynamicDocument):
    name = StringField(max_length=256)


class StudentList(DynamicDocument):
    type = StringField(max_length=256)
    list = ListField(ReferenceField(Student, reverse_delete_rule=PULL))

    def delete(self, *args, **kwargs):
        for student in self.list:
            student.delete()
        super(StudentList, self).delete(*args, **kwargs)


class Event(DynamicDocument):
    name = StringField(max_length=256)
    student_lists = ListField(ReferenceField(StudentList, reverse_delete_rule=PULL))


class File(Document):
    file = FileField()


class SingleLine(Document):
    single_input = DictField()
