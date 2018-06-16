from django.contrib import auth

from utils.views import APIView
from utils.constants import SUCCESS_RESPONSE_STRING, ERROR_RESPONSE_STRING

from account.serializers import UserRegisterSerializer
from account.models import User
from account.decorators import login_required

from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema


class UserRegisterAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: User register",
        request_body=UserRegisterSerializer,
        responses={200: SUCCESS_RESPONSE_STRING,
                   400: ERROR_RESPONSE_STRING}
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
            user = User.objects.create(username=data["username"], email=data["email"], user_type=data["user_type"],
                                       real_name=data['real_name'])
            user.set_password(data["password"])
            user.save()
            return self.success("Succeeded")
        else:
            return self.invalid_serializer(serializer)


class TestDecoratorsAPI(APIView):
    permission_classes = [login_required]
    from rest_framework_jwt.authentication import JSONWebTokenAuthentication
    authentication_classes = [JSONWebTokenAuthentication]

    @swagger_auto_schema(
        operation_description="API: test",
        responses={200: SUCCESS_RESPONSE_STRING,
                   400: ERROR_RESPONSE_STRING}
    )
    def get(self, request):
        user = request.user
        return self.success(user.username)
