from rest_framework_mongoengine.serializers import DynamicDocumentSerializer
from .models import Event, Student, StudentList


class EventSerializer(DynamicDocumentSerializer):

    class Meta:
        model = Event
        exclude = ('student_lists', )

    def create(self, validated_data):
        student_lists = validated_data.pop('student_lists')
        event = Event(**validated_data)
        for student_list in student_lists:
            list = student_list.pop('list')
            li = StudentList(**student_list)
            for each in list:
                stu = Student(**each)
                stu.save()
                li.list.append(stu)
            li.save()
            event.student_lists.append(li)
            event.save()
        return event
