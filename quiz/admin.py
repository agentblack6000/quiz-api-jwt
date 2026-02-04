from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Teacher

# Register your models here.
@admin.register(Teacher)
class TeacherRegistration(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        teacher_group = Group.objects.get(name="teacher")
        obj.user.groups.add(teacher_group)

        student_group = Group.objects.get(name="student")
        obj.user.groups.remove(student_group)
