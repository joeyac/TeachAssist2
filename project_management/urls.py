from django.urls import path
from project_management.views import SRTPProjectCreationAPI, GraProjectCreationAPI, GraProjectDeletionAPI


urlpatterns = [
    path('SRTPCreation/', SRTPProjectCreationAPI.as_view(), name='SRTPCreation'),
    path('GraCreation/', GraProjectCreationAPI.as_view(), name='GraCreation'),
    path('GraDeletion/', GraProjectDeletionAPI.as_view(), name='GraDeletion'),
]
