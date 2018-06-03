from django.urls import path
from account.views import UserLoginAPI, UserRegisterAPI, UserLogoutAPI

urlpatterns = [
    path('login/', UserLoginAPI.as_view(), name='login'),
    path('register/', UserRegisterAPI.as_view(), name='register'),
    path('logout/', UserLogoutAPI.as_view(), name='logout'),
]
