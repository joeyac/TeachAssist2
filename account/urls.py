from django.urls import path
from account.views import *


from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
urlpatterns = [
    path('register/', UserRegisterAPI.as_view(), name='register'),
    path('login/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),
    path('verify/', verify_jwt_token),

    path('test/', TestDecoratorsAPI.as_view(), name='test')
]
