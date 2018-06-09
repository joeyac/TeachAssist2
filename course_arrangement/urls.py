from django.urls import path
from course_arrangement.views import *

urlpatterns = [
    path('create_requirement/', RequirementCreateAPI.as_view(), name='create_requirement')
]
