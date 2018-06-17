from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser

from course_arrangement.algorithm_lab import solver
from course_arrangement.models import *
from course_arrangement.serializers import *
from utils.constants import AlgorithmStatus
from utils.constants import SUCCESS_RESPONSE_STRING, ERROR_RESPONSE_STRING
from utils.views import APIView


class ExecuteAssignmentAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: execute assignment algorithm",
        request_body=WeekDaySlotSerializer,
        responses={200: SUCCESS_RESPONSE_STRING,
                   400: {"error": None, "data": {'success': True, 'info': 'info', 'preference': 10.0}}.__str__()}
    )
    def post(self, request):
        serializer = WeekDaySlotSerializer(data=request.data)
        if serializer.is_valid():

            if cache.get('ALGO_STATUS') == AlgorithmStatus.RUNNING:
                return self.error('assignment is running')
            cache.set('ALGO_STATUS', AlgorithmStatus.RUNNING)

            week = serializer.data['week']
            day = serializer.data['day']
            slot = serializer.data['slot']
            solver.load_data(week=week, day=day, time_slot=slot)
            success = solver.run()
            info = solver.write_to_database()
            preference = solver.get_objective_value()
            data = {
                'success': success,
                'info': info,
                'preference': preference
            }

            cache.set('ALGO_STATUS', AlgorithmStatus.IDLE)

            return self.success(data)
        else:
            return self.invalid_serializer(serializer)


class ReExecuteAssignmentAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: re-execute assignment algorithm",
        responses={200: SUCCESS_RESPONSE_STRING,
                   400: {"error": None, "data": {'success': True, 'info': 'info', 'preference': 10.0}}.__str__()}
    )
    def get(self, request):
        if cache.get('ALGO_STATUS') == AlgorithmStatus.RUNNING:
            return self.error('assignment is running')
        if cache.get('ALGO_STATUS') == AlgorithmStatus.NEW:
            return self.error('you should run execute assignment first')
        try:
            cache.set('ALGO_STATUS', AlgorithmStatus.RUNNING)
            success = solver.run_another_optimal()
            info = solver.write_to_database()
            preference = solver.get_objective_value()
            data = {
                'success': success,
                'info': info,
                'preference': preference
            }
            cache.set('ALGO_STATUS', AlgorithmStatus.IDLE)
            return self.success(data)
        except Exception as e:
            return self.error(str(e))


class ShowTimeTableByClassAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: show time table by class, need class id",
        request_body=ClassAssignmentSerializer,
        responses={200: AssignmentSerializer(many=True),
                   400: ERROR_RESPONSE_STRING}
    )
    def post(self, request):
        serializer = ClassAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            if cache.get('ALGO_STATUS') == AlgorithmStatus.RUNNING:
                return self.error('assignment is running')

            cls = Class.objects.get(id=serializer.data['cid'])
            assignments = Assignment.objects.filter(course__classes__in=[cls])
            data = AssignmentSerializer(instance=assignments, many=True).data
            return self.success(data)
        else:
            return self.invalid_serializer(serializer)


class ShowTimeTableByClassRoomAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: show time table by class room, need class room id",
        request_body=ClassRoomAssignmentSerializer,
        responses={200: AssignmentSerializer(many=True),
                   400: ERROR_RESPONSE_STRING}
    )
    def post(self, request):
        serializer = ClassRoomAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            if cache.get('ALGO_STATUS') == AlgorithmStatus.RUNNING:
                return self.error('assignment is running')

            classroom = ClassRoom.objects.get(id=serializer.data['rid'])
            assignments = Assignment.objects.filter(classroom=classroom)
            data = AssignmentSerializer(instance=assignments, many=True).data
            return self.success(data)
        else:
            return self.invalid_serializer(serializer)


class ShowTimeTableByTeacherAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: show time table by teacher, need teacher id",
        request_body=TeacherAssignmentSerializer,
        responses={200: AssignmentSerializer(many=True),
                   400: ERROR_RESPONSE_STRING}
    )
    def post(self, request):
        serializer = TeacherAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            if cache.get('ALGO_STATUS') == AlgorithmStatus.RUNNING:
                return self.error('assignment is running')

            teacher = User.objects.get(id=serializer.data['tid'], user_type=UserType.TEACHER)
            assignments = Assignment.objects.filter(course__teacher=teacher)
            data = AssignmentSerializer(instance=assignments, many=True).data
            return self.success(data)
        else:
            return self.invalid_serializer(serializer)


class GetTeacherListAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: get teacher list",
        responses={200: TeacherSerializer(many=True),
                   400: ERROR_RESPONSE_STRING}
    )
    def get(self, request):
        teachers = User.objects.all().filter(user_type=UserType.TEACHER)
        data = TeacherSerializer(instance=teachers, many=True).data
        return self.success(data)


class GetClassListAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: get class list",
        responses={200: ClassSerializer(many=True),
                   400: ERROR_RESPONSE_STRING}
    )
    def get(self, request):
        data = ClassSerializer(instance=Class.objects.all(), many=True).data
        return self.success(data)


class GetClassRoomListAPI(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: get class list",
        responses={200: ClassRoomSerializer(many=True),
                   400: ERROR_RESPONSE_STRING}
    )
    def get(self, request):
        data = ClassRoomSerializer(instance=ClassRoom.objects.all(), many=True).data
        return self.success(data)
