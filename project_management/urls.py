from django.urls import path
from project_management.views import *


urlpatterns = [
    path('SRTPCreation/', SRTPProjectCreationAPI.as_view(), name='SRTPCreation'),
    path('SRTPUpdate/', SRTPUpdateAPI.as_view(), name='SRTPUpdate'),
    path('FileUpload/', FileUploadAPI.as_view(), name='FileUpload'),
    path('SRTPFindSelf/', SRTPFindSelfAPI.as_view(), name='SRTPFindSelf'),
    path('SRTPGetSelf/', SRTPGetSelfAPI.as_view(), name='SRTPGetSelf'),

    path('SRTPStateChange/', SRTPStateChangeAPI.as_view(), name='SRTPStateChange'),
    path('SRTPLevelChange/', SRTPLevelChangeAPI.as_view(), name='SRTPLevelChange'),
    path('SRTPFindAll/', SRTPFindAllAPI.as_view(), name='SRTPFindAll'),
    path('SRTPGetALL/', SRTPGetALLAPI.as_view(), name='SRTPGetALL'),

    path('GraProjectCreation/', GraProjectCreationAPI.as_view(), name='GraProjectCreation'),
    path('GraUpdate/', GraUpdateAPI.as_view(), name='GraUpdate'),
    path('GraGetSelf/', GraGetSelfAPI.as_view(), name='GraGetSelf'),

    path('GraStateChange/', GraStateChangeAPI.as_view(), name='GraStateChange'),
    path('GraGetALL/', GraGetALLAPI.as_view(), name='GraGetALL'),
    # path('GraProjectCreation/', GraProjectCreationAPI.as_view(), name='GraProjectCreation'),
    # path('GraProjectCreation/', GraProjectCreationAPI.as_view(), name='GraProjectCreation'),
    # path('GraProjectCreation/', GraProjectCreationAPI.as_view(), name='GraProjectCreation'),
    # path('GraProjectCreation/', GraProjectCreationAPI.as_view(), name='GraProjectCreation'),
    # path('GraProjectCreation/', GraProjectCreationAPI.as_view(), name='GraProjectCreation'),
]
