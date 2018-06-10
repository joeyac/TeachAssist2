from django.shortcuts import render

# Create your views here.
from utils.views import APIView
from utils.serializers import SuccessResponseSerializer, ErrorResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from project_management.models import SRTPProject, File_Info, EduProject, GraProject
from utils.constants import FileType, ProStage, UserType
from account.models import User
# from account.decorators import student_required
import django.utils.timezone as timezone


'''---------------------------SRTP项目部分---------------------------------------'''


class SRTPProjectCreationAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: srtp  project creation",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        # serializer = UserLoginSerializer(data=request.data)
        data = request.data
        user = request.user
        f = request.FILES
        # print(f)
        if not f:
            return self.success("NO files")
        stu = User.objects.get(username=user.username)
        '''
        测试用代码
        '''
        if stu.srtp_project is not None:
            return self.success("repeated creation operation!")

        srtp_project = SRTPProject.objects.create()
        # srtp_project.crate_time = timezone.now()
        srtp_project.update_time = timezone.now()
        srtp_project.save()
        file_url = '../upgrade/' + data['filename']
        file_info = File_Info.objects.create(file_name=data['filename'], file_url=file_url, project=srtp_project)
        file_info.save()
        stu.srtp_project = srtp_project
        stu.save()
        try:
            return self.success("Succeeded")
        except:
            return self.error("ERROR")


class SRTPProjectInitFileDeletionAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: SRTP project delete initial file",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        '''
        用户必须有一个项目,
        必须存在项目申请表,将所有的项目申请表都删掉
        :param request:
        :return:
        '''
        # data = request.data
        user = request.user
        '''
        先找到原来的申请表
        '''
        srtp_project = User.objects.filter(username=user.username)
        origin_files = File_Info.objects.filter(project=srtp_project, pro_stage=ProStage.INIT)
        origin_files.all().delete()
        return self.success("Successed")


class SRTPProjectInitFileUploadAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: SRTP project upload initial file",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        '''
        用户必定会有一个项目
        1. 删除之前的文件
        2. 添加现在的文件
        3. 那么必须有删除文件的操作
        :param request:
        :return:
        '''
        data = request.data
        user = request.user

        files = request.FILES
        srtp_project = User.objects.filter(username=user.username)

        origin_files = File_Info.objects.filter(project=srtp_project, pro_stage=ProStage.INIT)
        origin_files.all().delete()

        if not files:
            return self.error("NO files")

        file_url_bind = '../upload/'
        cnt = 1
        for file in files:
            file_url = file_url_bind+str(cnt)+'_'+file
            init_file = File_Info.objects.create(file_name=file, file_url=file_url, project=srtp_project, pro_stage=ProStage.INIT)
            init_file.save()
            cnt += 1
        return self.success("Successed")


class SRTPProjectMidFileUploadAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: SRTP project upload Midterm file",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        '''
        用户必定会有一个项目
        1. 删除之前的文件
        2. 添加现在的文件
        3. 那么必须有删除文件的操作
        :param request:
        :return:
        '''
        data = request.data
        user = request.user

        files = request.FILES
        srtp_project = User.objects.filter(username=user.username)

        origin_files = File_Info.objects.filter(project=srtp_project, pro_stage=ProStage.MID)
        origin_files.all().delete()

        if not files:
            return self.error("NO files")

        file_url_bind = '../upload/'
        cnt = 1
        for file in files:
            file_url = file_url_bind+str(cnt)+'_'+file
            init_file = File_Info.objects.create(file_name=file, file_url=file_url, project=srtp_project, pro_stage=ProStage.MID)
            init_file.save()
            cnt += 1
        return self.success("Successed")


class SRTPProjectMidFileDeletionAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: SRTP project delete Midterm file",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        '''
        用户必须有一个项目,
        必须存在项目申请表,将所有的项目申请表都删掉
        :param request:
        :return:
        '''
        # data = request.data
        user = request.user
        '''
        先找到原来的申请表
        '''
        srtp_project = User.objects.filter(username=user.username)
        origin_files = File_Info.objects.filter(project=srtp_project, pro_stage=ProStage.MID)
        origin_files.all().delete()
        return self.success("Successed")


class SRTPProjectFINFileUploadAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: SRTP project upload Final file",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        '''
        用户必定会有一个项目
        1. 删除之前的文件
        2. 添加现在的文件
        3. 那么必须有删除文件的操作
        :param request:
        :return:
        '''
        data = request.data
        user = request.user

        files = request.FILES
        srtp_project = User.objects.filter(username=user.username)

        origin_files = File_Info.objects.filter(project=srtp_project, pro_stage=ProStage.FIN)
        origin_files.all().delete()

        if not files:
            return self.error("NO files")

        file_url_bind = '../upload/'
        cnt = 1
        for file in files:
            file_url = file_url_bind+str(cnt)+'_'+file
            init_file = File_Info.objects.create(file_name=file, file_url=file_url, project=srtp_project, pro_stage=ProStage.FIN)
            init_file.save()
            cnt += 1
        return self.success("Successed")


class SRTPProjectFINFileDeletionAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: SRTP project delete Final file",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        '''
        用户必须有一个项目,
        必须存在项目申请表,将所有的项目申请表都删掉
        :param request:
        :return:
        '''
        # data = request.data
        user = request.user
        '''
        先找到原来的申请表
        '''
        srtp_project = User.objects.filter(username=user.username)
        origin_files = File_Info.objects.filter(project=srtp_project, pro_stage=ProStage.FIN)
        origin_files.all().delete()
        return self.success("Successed")


'''---------------------------教改项目部分---------------------------------------
教改项目和SRTP项目一样,只是用户换成教师,但具体的内容可能需要在后续的编写中解决'''
'''---------------------------毕业论文项目部分------------------------------------'''


class GraProjectCreationAPI(APIView):
    @swagger_auto_schema(
        operation_description="API: Graduation project creation",
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        data = request.data
        user = request.user
        if user.gra_project is not None:
            return self.error("Creation repeated")
        gra_project = GraProject.objects.create()
        gra_project.update_time=timezone.now()
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
        # query_serializer=student_required,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        data = request.data
        user = request.user

        gra_project = user.gra_project
        if gra_project is None:
            return self.error("there is no project")
        members = User.objects.filter(gra_project=gra_project)
        for member in members:
            member.gra_project=None
            member.save()
        GraProject.objects.get(id=gra_project.id).delete()
        return self.success("Succeed")


'''-----------------------------秘书审阅表-查询-修改状态-修改等级------------------------'''
