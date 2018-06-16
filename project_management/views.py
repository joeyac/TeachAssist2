from utils.views import APIView
from utils.serializers import SuccessResponseSerializer, ErrorResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from account.decorators import *
from rest_framework.parsers import MultiPartParser
from project_management.serializers import *

'''---------------------------SRTP项目部分---------------------------------------'''


class SRTPProjectCreationAPI(APIView):
    permission_classes = [student_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP  project creation",
        request_body=SRTPProjectCreationSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPProjectCreationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            PIC = User.objects.filter(username=data['username']).first()
            srtp_project = SRTPProject.objects.create(pro_level=data["pro_level"],
                                                      person_in_charge=PIC,
                                                      members=data["members"],
                                                      instructor=data['instructor'],
                                                      apply_file=data['file_url'],
                                                      pro_name=data['pro_name'],
                                                      introduction=data['introduction'],
                                                      create_year=data['create_year'],
                                                      end_year=data['end_year'])
            srtp_project.save()
            return self.success(srtp_project.toDict())
        else:
            return self.invalid_serializer(serializer)


class SRTPFindSelfAPI(APIView):
    '''
    得到自己管理的项目的简略信息
    '''
    permission_classes = [student_required]

    @swagger_auto_schema(
            operation_description="API: SRTP project find",
            responses={200: SuccessResponseSerializer,
                       400: ErrorResponseSerializer}
        )
    def get(self, request):
        user = request.user
        PIC = User.objects.filter(username=user.username).first()
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC).first()
        if srtp_pro is None:
            return self.success("There is no project")
        else:
            return self.success({'id': srtp_pro.id, 'pro_name': srtp_pro.pro_name, 'person_in_charge': PIC.username,
                             'create_year': srtp_pro.create_year, 'pro_state': srtp_pro.pro_state,
                             'pro_level': srtp_pro.pro_level})


class SRTPGetSelfAPI(APIView):
    '''
    得到自己管理的项目的详细信息
    '''
    permission_classes = [student_required]

    @swagger_auto_schema(
            operation_description="API: SRTP project find",
            responses={200: SuccessResponseSerializer,
                       400: ErrorResponseSerializer}
        )
    def get(self, request):
        user = request.user
        PIC = User.objects.filter(username=user.username).first()
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC).first()
        if srtp_pro is None:
            return self.success("There is no project")
        else:
            return self.success(srtp_pro.toDict())


class FileUploadAPI(APIView):
    permissions = [student_required, teacher_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project information update",
        request_body=FileUploadSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get('file')
            file_url = settings.MEDIA_ROOT + file.name
            print(file_url)
            with open(file_url, 'wb') as f:
                for line in file.chunks():
                    f.write(line)
                f.close()
            return self.success(file_url)
        else:
            return self.invalid_serializer(serializer)


class SRTPUpdateAPI(APIView):
    permissions = [student_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project information update",
        request_body=SRTPUpdateSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
            members = data['members']
            instructor = data['instructor']
            introduction = data['introduction']
            file_url = data['file_url']
            if members:
                srtp_pro.members = members
            if instructor:
                srtp_pro.instructor = instructor
            if introduction:
                srtp_pro.introduction = introduction
            operation = data['op_code']
            if operation == OperationCode.UPLOAD_INT:
                    srtp_pro.apply_file = file_url
                    srtp_pro.pro_state = ProState.UNCONFIRMED
            elif operation == OperationCode.UPLOAD_MID:
                    srtp_pro.middle_file = file_url
                    srtp_pro.pro_state = ProState.MIDTERM_CHECKING
            elif operation == OperationCode.UPLOAD_FIN:
                    srtp_pro.end_file = file_url
                    srtp_pro.pro_state = ProState.FINAL_CHEKING
            elif operation == OperationCode.UPLOAD_TER:
                    srtp_pro.abnormal_file = file_url
                    srtp_pro.pro_state = ProState.TERMINATED
            elif operation == OperationCode.UPLOAD_POS:
                    srtp_pro.abnormal_file = file_url
                    srtp_pro.pro_state = ProState.POSTPONED
            srtp_pro.save()

            return self.success(srtp_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


'''---------------------------教改项目部分---------------------------------------
教改项目和SRTP项目一样,只是用户换成教师,但具体的内容可能需要在后续的编写中解决'''
'''---------------------------毕业论文项目部分------------------------------------'''


class GraProjectCreationAPI(APIView):
    permission_classes = [student_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP  project creation",
        request_body=GraProjectCreationSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = GraProjectCreationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            PIC = User.objects.filter(id=data['PIC_id']).first()
            # 保存文件
            file = request.FILES['file1']
            srtp_project = SRTPProject.objects.create(pro_level=data["pro_level"],
                                                      person_in_charge=PIC,
                                                      members=data["members"],
                                                      instructor=data['instructor'],
                                                      file1=file,
                                                      pro_name=data['pro_name'],
                                                      introduction=data['introduction'],
                                                      create_year=data['create_year'],
                                                      end_year=data['end_year'])
            srtp_project.save()
            return self.success(srtp_project.toDict())
        else:
            return self.invalid_serializer(serializer)


'''-----------------------------秘书审阅表-查询-修改状态-修改等级------------------------'''


class SRTPStateChangeAPI(APIView):
    permissions = [secretary_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        request_body=SRTPStateChangeSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPStateChangeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
            op_code = data['op_code']
            if op_code == OperationCode.CREATION_PASS:
                srtp_pro.pro_state = ProState.APPLY_PASSED
            elif op_code == OperationCode.FIN_PASS:
                srtp_pro.pro_state = ProState.DONE
            elif op_code == OperationCode.MID_PASS:
                srtp_pro.pro_state = ProState.MIDTERM_PASSED
            elif op_code == OperationCode.REJECT:
                srtp_pro.pro_state = ProState.TERMINATED
            srtp_pro.save()
            return self.success(srtp_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


class SRTPLevelChangeAPI(APIView):
    permissions = [secretary_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        request_body=SRTPLevelChangeSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPLevelChangeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.filter(id=data['pro_id']).first()
            srtp_pro.pro_level = data['pro_level']
            srtp_pro.save()
            return self.success(srtp_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


class SRTPFindAllAPI(APIView):
    permissions = [secretary_required]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        # request_body=SRTPStateChangeSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        srtp_pros = SRTPProject.objects.all()
        if srtp_pros is None:
            return self.success("no project exist!")
        single_pro = []
        total_pro = []
        for srtp_pro in srtp_pros:
            single_pro.append(srtp_pro.PIC_id)
            single_pro.append(srtp_pro.create_year)
            single_pro.append(srtp_pro.end_year)
            single_pro.append(srtp_pro.pro_level)
            single_pro.append(srtp_pro.members)
            single_pro.append(srtp_pro.pro_name)
            single_pro.append(srtp_pro.introduction)
            single_pro.append(srtp_pro.instructor)
            total_pro.append(single_pro)
            single_pro = []
        return self.success(total_pro)


class SRTPGetAPI(APIView):
    permissions = [secretary_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        request_body=SRTPGetSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPGetSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.get(id=data['pro_id'])
            return self.success(srtp_pro.toDict())
        else:
            return self.invalid_serializer(serializer)