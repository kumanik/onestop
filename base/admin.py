from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
  list_display = ('name','email')
