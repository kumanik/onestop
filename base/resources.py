from import_export import resources
from .models import Student

class Studentres(resources.ModelResource):
  class meta:
    model = Student
