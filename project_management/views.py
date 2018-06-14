from utils.views import APIView
from utils.serializers import SuccessResponseSerializer, ErrorResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from project_management.models import SRTPProject, EduProject, GraProject
from utils.constants import FileType, ProStage, UserType
from account.models import User
from account.decorators import *
from rest_framework.parsers import MultiPartParser
import django.utils.timezone as timezone
from project_management.serializers import SRTPProjectCreationSerializer, SRTPProjectInitFileUploadSerializer

'''---------------------------SRTP项目部分---------------------------------------'''


class SRTPProjectCreationAPI(APIView):
    permission_classes = [login_required, student_required]
    # parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: srtp  project creation",
        request_body=SRTPProjectCreationSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPProjectCreationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            srtp_project = SRTPProject.objects.create(pro_level=data["pro_level"],
                                                      person_in_charge=data['person_in_charge'],
                                                      members=data["members"],
                                                      file1=data['file'],
                                                      pro_name=data['pro_name'],
                                                      introduction=data['introducton'],
                                                      create_year=data['create_year'],
                                                      end_year=data['end_year'])
            # srtp_project.update_time = timezone.now()
            srtp_project.save()
            return self.success("Succeeded")
        else:
            return self.invalid_serializer(serializer)


class SRTPProjectInitFileDeletionAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: SRTP project delete initial file",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        """
        用户必须有一个项目,
        必须存在项目申请表,将所有的项目申请表都删掉
        """
        # data = request.data
        user = request.user
        '''
        先找到原来的申请表
        '''
        srtp_project = User.objects.filter(username=user.username)
        if srtp_project is None:
            return self.error("there is no project!")
        return self.success("Succeed")


class SRTPProjectInitFileUploadAPI(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project upload initial file",
        request_body=SRTPProjectInitFileUploadSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPProjectInitFileUploadSerializer(data=request.data)
        '''
        用户必定会有一个项目
        1. 删除之前的文件
        2. 添加现在的文件
        3. 那么必须有删除文件的操作
        '''
        if serializer.is_valid():
            data = serializer.data
            user = serializer.user

            files = data['file']
            srtp_project = User.objects.filter(username=user.username)

            if srtp_project is None:
                return self.error("there is no match project!")

            cnt = 1
            for file in files:
                cnt += 1
            return self.success("Succeed")
        else:
            return self.invalid_serializer(serializer)


'''---------------------------教改项目部分---------------------------------------
教改项目和SRTP项目一样,只是用户换成教师,但具体的内容可能需要在后续的编写中解决'''
'''---------------------------毕业论文项目部分------------------------------------'''


class GraProjectCreationAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: Graduation project creation",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        data = request.data
        user = request.user
        if user.gra_project is not None:
            return self.error("Creation repeated")
        gra_project = GraProject.objects.create()
        gra_project.update_time = timezone.now()
        gra_project.save()
        # print(user.user_type)
        if user.user_type == UserType.TEACHER:
            # print(user.user_type)
            student_ID = data["student_ID"]
            teacher = User.objects.get(username=user.username)
            teacher.gra_project = gra_project
            teacher.save()
            student = User.objects.get(username=student_ID)
            student.gra_project = gra_project
            student.save()
        elif user.user_type == UserType.STUDENT:
            # print(user.user_type)
            teacher_ID = data["teacher_ID"]
            student = User.objects.get(username=user.username)
            student.gra_project = gra_project
            student.save()
            teacher = User.objects.get(username=teacher_ID)
            teacher.gra_project = gra_project
            teacher.save()

        return self.success("Succeed")


class GraProjectDeletionAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: Graduation project deletion",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        user = request.user
        gra_project = user.gra_project
        if gra_project is None:
            return self.error("there is no project")
        members = User.objects.filter(gra_project=gra_project)
        for member in members:
            member.gra_project = None
            member.save()
        GraProject.objects.get(id=gra_project.id).delete()
        return self.success("Succeed")


'''-----------------------------秘书审阅表-查询-修改状态-修改等级------------------------'''
