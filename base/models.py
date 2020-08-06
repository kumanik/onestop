from mongoengine import fields, document


class Student(document.DynamicDocument):
    name = fields.StringField(max_length=256)
    meta = {'db_alias': 'default'}


class StudentList(document.DynamicDocument):
    type = fields.StringField(max_length=256)
    list = fields.ListField(fields.ReferenceField(
        Student, reverse_delete_rule=4))
    meta = {'db_alias': 'default'}

    def delete(self, *args, **kwargs):
        for student in self.list:
            student.delete()
        super(StudentList, self).delete(*args, **kwargs)


class Event(document.DynamicDocument):
    name = fields.StringField(max_length=256)
    student_lists = fields.ListField(fields.ReferenceField(
        StudentList, reverse_delete_rule=4))
    meta = {'db_alias': 'default'}

    def delete(self, *args, **kwargs):
        for list in self.student_lists:
            list.delete()
        super(Event, self).delete(*args, **kwargs)
