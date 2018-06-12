from django.urls import path
from course_arrangement.views import *

urlpatterns = [
    path('create_requirement/', RequirementCreateAPI.as_view(), name='create_requirement'),
    path('update_week_day_section/', UpdateWeekDaySectionAPI.as_view(), name='update_week_day_section'),

    path('atest', ATestAPI.as_view()),
]
