from drf_yasg.utils import swagger_auto_schema

from utils.constants import SUCCESS_RESPONSE_STRING, ERROR_RESPONSE_STRING
from utils.views import APIView

from course_arrangement.serializers import *
from course_arrangement.models import *


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


class UpdateWeekDaySectionAPI(APIView):

    @swagger_auto_schema(
        operation_description="API: update week day period, notice this will destroy all existed period",
        request_body=UpdateWeekDaySectionSerializer,
        responses={200: SUCCESS_RESPONSE_STRING,
                   400: ERROR_RESPONSE_STRING}
    )
    def post(self, request):
        serializer = UpdateWeekDaySectionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            weeks = data['weeks']
            days = data['days']
            sections = data['sections']
            Period.objects.all().delete()
            for i in range(1, weeks + 1):
                for j in range(1, days + 1):
                    for k in range(1, sections + 1):
                        Period.objects.create(week=i, day=j, section=k)
            # 所有对应的lecture都被级联删除了，重新生成
            periods = Period.objects.all()
            classrooms = ClassRoom.objects.all()
            for period in periods:
                for classroom in classrooms:
                    Lecture.objects.create(period=period, classroom=classroom)
            return self.success()
        else:
            return self.invalid_serializer(serializer)




class ATestAPI(APIView):

    def get(self, request):
        from utils.algorithm import execute
        return self.success(execute())
