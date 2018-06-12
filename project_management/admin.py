from django.contrib import admin

# Register your models here.
from project_management.models import SRTPProject, File_Info, GraProject, EduProject

admin.site.register(SRTPProject)
admin.site.register(File_Info)
admin.site.register(GraProject)
admin.site.register(EduProject)