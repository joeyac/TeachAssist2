from utils.views import APIView
from utils.serializers import SuccessResponseSerializer, ErrorResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from project_management.models import SRTPProject, EduProject, GraProject
from utils.constants import FileType, ProStage, UserType
from account.decorators import *
from rest_framework.parsers import MultiPartParser
import django.utils.timezone as timezone
from project_management.serializers import *

'''---------------------------SRTP项目部分---------------------------------------'''


class SRTPProjectCreationAPI(APIView):
    permission_classes = [student_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: 1. SRTP  project creation",
        request_body=SRTPProjectCreationSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPProjectCreationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            PIC = User.objects.filter(username=data['PIC_id']).first()
            # 保存文件
            file = request.FILES['file1']
            # print(file)
            # print(file.size)
            # file_url =  '../static/upload/'
            # f = open(file_url+file.name, 'wb')
            # for line in file.chunks():
            #     f.write(line)
            # f.close()
            srtp_project = SRTPProject.objects.create(pro_level=data["pro_level"],
                                                      person_in_charge=PIC,
                                                      members=data["members"],
                                                      instructor=data['instructor'],
                                                      file1=file,
                                                      pro_name=data['pro_name'],
                                                      introduction=data['introduction'],
                                                      create_year=data['create_year'],
                                                      end_year=data['end_year'])
            # srtp_project.update_time = timezone.now()
            # srtp_project.file1.save(file.name, file)
            # print(srtp_project.file1.name)
            srtp_project.save()
            return self.success("Succeeded")
        else:
            return self.invalid_serializer(serializer)


class SRTPFindAPI(APIView):
    permission_classes = [student_required]

    @swagger_auto_schema(
            operation_description="API: 2. SRTP project find",
            request_body=SRTPFindSerializer,
            responses={200: SuccessResponseSerializer,
                       400: ErrorResponseSerializer}
        )
    def post(self, request):
        serializer = SRTPFindSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            PIC = User.objects.filter(username=data['PCI_id']).first()
            srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC).first()
            if srtp_pro is None:
                return self.success("There is no project")
            return self.success({'id': srtp_pro.id, 'pro_name': srtp_pro.pro_name, 'person_in_charge': PIC.username,
                                 'create_year': srtp_pro.create_year, 'pro_state': srtp_pro.pro_state,
                                 'pro_level': srtp_pro.pro_level})
        else:
            return self.invalid_serializer(serializers)


class SRTPProjectFileUploadAPI(APIView):
    parser_classes = [MultiPartParser]
    permissions = [student_required]

    @swagger_auto_schema(
        operation_description="API: 3. SRTP project upload initial file",
        request_body=SRTPProjectFileUploadSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPProjectFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.get(id=data['pro_id'])
            file = request.FILES['file']
            pro_stage = data['pro_stage']
            if pro_stage == ProStage.INIT:
                srtp_pro.file1 = file
            elif pro_stage == ProStage.MID:
                srtp_pro.file2 = file
            else:
                srtp_pro.file3 = file
            srtp_pro.save()
            return self.success("Succeed")
        else:
            return self.invalid_serializer(serializer)


class SRTPUpdateAPI(APIView):
    permissions = [student_required]

    @swagger_auto_schema(
        operation_description="API: 4. SRTP project information update",
        request_body=SRTPUpdateSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
            members = data['members']
            instructor = data['instructor']
            introduction = data['introduction']
            if members:
                srtp_pro.members = members
                srtp_pro.pro_state = ProState.APPLYING
            if instructor:
                srtp_pro.instructor = instructor
                srtp_pro.pro_state = ProState.MIDTERM_CHECKING
            if introduction:
                srtp_pro.introduction = introduction
                srtp_pro.pro_state = ProState.FINAL_CHEKING
            srtp_pro.save()
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
