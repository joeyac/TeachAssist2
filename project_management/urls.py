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
    path('SRTPGetAll/', SRTPGetAllAPI.as_view(), name='SRTPGetAll'),

    path('GraProjectCreation/', GraProjectCreationAPI.as_view(), name='GraProjectCreation'),
    path('GraUpdate/', GraUpdateAPI.as_view(), name='GraUpdate'),
    path('GraGetSelf/', GraGetSelfAPI.as_view(), name='GraGetSelf'),

    path('GraStateChange/', GraStateChangeAPI.as_view(), name='GraStateChange'),
    path('GraGetAll/', GraGetAllAPI.as_view(), name='GraGetALL'),

    path('EduCreation/', SRTPProjectCreationAPI.as_view(), name='SRTPCreation'),
    path('EduUpdate/', EduUpdateAPI.as_view(), name='EduUpdate'),
    path('EduGetSelf/', EduGetSelfAPI.as_view(), name='EduGetSelf'),

    path('EduStateChange/', EduStateChangeAPI.as_view(), name='EduStateChange'),
    path('EduLevelChange/', EduLevelChangeAPI.as_view(), name='EduLevelChange'),
    path('EduFindAll/', EduFindAllAPI.as_view(), name='EduFindAll'),
    path('EduGetAll/', EduGetAllAPI.as_view(), name='EduGetALL'),
]
