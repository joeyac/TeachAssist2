from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from utils.constants import SUCCESS_RESPONSE_STRING, ERROR_RESPONSE_STRING
from utils.views import APIView

from course_arrangement.serializers import *


class RequirementCreateAPI(APIView):

    @swagger_auto_schema(
        operation_description="API: Create Requirement",
        request_body=RequirementCreateSerializer,
        responses={200: SUCCESS_RESPONSE_STRING,
                   400: ERROR_RESPONSE_STRING}
    )
    def post(self, request):
        serializer = RequirementCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            lecture = Requirement.objects.filter(id=data['lecture_id']).first()
            teacher = User.objects.filter(id=data['teacher_id'], user_type=UserType.TEACHER).first()
            instance = Requirement.objects.create(favorite=data['favorite'], lecture=lecture, teacher=teacher)
            instance.save()
            return self.success("create requirement success")
        else:
            return self.invalid_serializer(serializer)
