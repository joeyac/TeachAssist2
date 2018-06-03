from django.contrib import auth

from utils.views import APIView, validate_serializer

from account.serializers import UserRegisterSerializer, UserLoginSerializer
from account.models import User


class UserRegisterAPI(APIView):

    @validate_serializer(UserRegisterSerializer)
    def post(self, request):
        """
        User register api
        """
        data = request.data
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()
        if User.objects.filter(username=data["username"]).exists():
            return self.error("Username already exists")
        if User.objects.filter(email=data["email"]).exists():
            return self.error("Email already exists")
        user = User.objects.create(username=data["username"], email=data["email"], user_type=data["user_type"])
        user.set_password(data["password"])
        user.save()
        return self.success("Succeeded")


class UserLoginAPI(APIView):

    @validate_serializer(UserLoginSerializer)
    def post(self, request):
        """
        User login api
        """
        data = request.data
        user = auth.authenticate(username=data["username"], password=data["password"])
        # None is returned if username or password is wrong
        if user:
            if not user.is_active:
                return self.error("Your account has been disabled")
            auth.login(request, user)
            return self.success("Succeeded")

        else:
            return self.error("Invalid username or password")


class UserLogoutAPI(APIView):

    def get(self, request):
        auth.logout(request)
        return self.success()
