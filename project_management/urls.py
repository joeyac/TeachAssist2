from django.urls import path
from project_management.views import *


urlpatterns = [
    path('SRTPCreation/', SRTPProjectCreationAPI.as_view(), name='SRTPCreation'),
    path('SRTPUpdate/', SRTPUpdateAPI.as_view(), name='SRTPUpdate'),
    path('GraCreation/', GraProjectCreationAPI.as_view(), name='GraCreation'),
    # path('GraDeletion/', GraProjectDeletionAPI.as_view(), name='GraDeletion'),
]
