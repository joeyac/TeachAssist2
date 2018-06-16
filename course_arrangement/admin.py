from django.contrib import admin
from course_arrangement.models import Course, ClassRoom, Class, Assignment, ClassRoomCollegeChoice, ClassRoomFloorChoice


class classRoomAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'capacity')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher_name', 'course_name', 'classroom_name', 'week', 'day', 'slot')
    list_filter = ('course__teacher', 'course', 'classroom',)

    def week(self, obj):
        return obj.course.week_str


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_lab', 'teacher_name', 'class_name', 'week_str',
                    'capacity', 'slots_per_week', 'max_slots_per_day')
    list_editable = ('is_lab', 'slots_per_week', 'max_slots_per_day')
    list_display_links = ('id', 'name',)
    list_filter = ('name', 'teacher', 'classes')


admin.site.register(Course, CourseAdmin)
admin.site.register(ClassRoom, classRoomAdmin)
admin.site.register(Class)
admin.site.register(Assignment, AssignmentAdmin)

admin.site.register(ClassRoomFloorChoice)

admin.site.register(ClassRoomCollegeChoice)
