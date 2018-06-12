from django.urls import path
from account.views import *

urlpatterns = [
    path('register/', UserRegisterAPI.as_view(), name='register'),

    path('test/', TestDecoratorsAPI.as_view(), name='test')
]
