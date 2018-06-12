from django.contrib import admin

# Register your models here.
from course_arrangement.models import Course, ClassRoom, Period, Class, Lecture, Requirement

admin.site.register(Course)
admin.site.register(ClassRoom)
admin.site.register(Class)
admin.site.register(Period)
admin.site.register(Lecture)
admin.site.register(Requirement)
