from django.urls import path
from project_management.views import *


urlpatterns = [
    path('SRTPCreation/', SRTPProjectCreationAPI.as_view(), name='SRTPCreation'),
    path('SRTPUpdate/', SRTPUpdateAPI.as_view(), name='SRTPUpdate'),
    path('FileUpload/', FileUploadAPI.as_view(), name='FileUpload'),
    path('SRTPFindSelf/', SRTPFindSelfAPI.as_view(), name='SRTPFindSelf'),
    path('SRTPGetSelf/', SRTPGetSelfAPI.as_view(), name='SRTPGetSelf'),

    path('SRTPStateChange/', SRTPStateChangeAPI.as_view(), name='SRTPStateChange'),
    path('SRTPLevelChang/', SRTPLevelChangeAPI.as_view(), name='SRTPLevelChange'),
    path('SRTPFindAll/', SRTPFindAllAPI.as_view(), name='SRTPFindAll'),
    path('SRTPGet/', SRTPGetAPI.as_view(), name='SRTPGet'),

    # path('GraDeletion/', GraProjectDeletionAPI.as_view(), name='GraDeletion'),
]
