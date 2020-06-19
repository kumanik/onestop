from rest_framework_mongoengine import serializers
from .models import *




class StudentSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentListSerializer(serializers.DynamicDocumentSerializer):
    class Meta:
        model = StudentList
        fields = '__all__'

class EventSerializer(serializers.DynamicDocumentSerializer):
        
    class Meta:
        model = Event
        fields = '__all__'

class FileSerializer(serializers.DocumentSerializer):
    class Meta:
        model = File
        fields = '__all__'