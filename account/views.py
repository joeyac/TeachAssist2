from django.contrib import auth

from utils.views import APIView
from utils.serializers import SuccessResponseSerializer, ErrorResponseSerializer

from account.serializers import UserRegisterSerializer, UserLoginSerializer
from account.models import User
from account.decorators import login_required

from drf_yasg.utils import swagger_auto_schema


class UserRegisterAPI(APIView):

    @swagger_auto_schema(
        operation_description="API: User register",
        query_serializer=UserRegisterSerializer,
        responses={200: SuccessResponseSerializer(data={"error": None, "data": "success"}),
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        """
        User register api
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
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
        else:
            return self.invalid_serializer(serializer)


class UserLoginAPI(APIView):

    @swagger_auto_schema(
        operation_description="API: User login",
        query_serializer=UserLoginSerializer,
        responses={200: SuccessResponseSerializer(data={"error": None, "data": "success"}),
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        """
        User login api
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = auth.authenticate(username=data["username"], password=data["password"])
            # None is returned if username or password is wrong
            if user:
                if not user.is_active:
                    return self.error("Your account has been disabled")
                auth.login(request, user)
                return self.success("Succeeded")

            else:
                return self.error("Invalid username or password")
        else:
            return self.invalid_serializer(serializer)


class UserLogoutAPI(APIView):

    def get(self, request):
        auth.logout(request)
        return self.success()


class TestDecoratorsAPI(APIView):

    @login_required
    def get(self, request):
        user = request.user
        return self.success(user.username)
