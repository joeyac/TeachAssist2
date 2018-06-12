from django.contrib import admin

# Register your models here.
from project_management.models import SRTPProject, GraProject, EduProject

admin.site.register(SRTPProject)
admin.site.register(GraProject)
admin.site.register(EduProject)