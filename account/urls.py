from django.urls import path
from account.views import *

urlpatterns = [
    path('login/', UserLoginAPI.as_view(), name='login'),
    path('register/', UserRegisterAPI.as_view(), name='register'),
    path('logout/', UserLogoutAPI.as_view(), name='logout'),

    path('test/', TestDecoratorsAPI.as_view(), name='test')
]
