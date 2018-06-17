from django.urls import path

from course_arrangement.views import *

urlpatterns = [
    path('timetable/teacher/', ShowTimeTableByTeacherAPI.as_view()),
    path('timetable/classroom/', ShowTimeTableByClassRoomAPI.as_view()),
    path('timetable/class/', ShowTimeTableByClassAPI.as_view()),

    path('assignment/execute/', ExecuteAssignmentAPI.as_view()),
    path('assignment/re-execute/', ReExecuteAssignmentAPI.as_view()),

    path('list/teacher/', GetTeacherListAPI.as_view()),
    path('list/classroom/', GetClassRoomListAPI.as_view()),
    path('list/class/', GetClassListAPI.as_view()),
]
