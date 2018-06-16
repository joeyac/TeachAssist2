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
        serializer = SRTPProjectCreationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data
            user = request.user
            PIC = User.objects.filter(id=user.id).first()
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
    permission_classes = [student_required]

    @swagger_auto_schema(
            operation_description="API: 找到自己负责的SRTP项目",
            responses={200: SuccessResponseSerializer,
                       400: ErrorResponseSerializer}
        )
    def get(self, request):
        user = request.user
        PIC = User.objects.filter(id=user.id).first()
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC).first()
        if srtp_pro is None:
            return self.success("There is no project")
        else:
            return self.success({'id': srtp_pro.id, 'pro_name': srtp_pro.pro_name, 'person_in_charge': PIC.username,
                                 'create_year': srtp_pro.create_year, 'pro_state': srtp_pro.pro_state,
                                 'pro_level': srtp_pro.pro_level})


class SRTPGetSelfAPI(APIView):
    permission_classes = [student_required]

    @swagger_auto_schema(
            operation_description="API: 得到自己管理的项目的详细信息",
            responses={200: SuccessResponseSerializer,
                       400: ErrorResponseSerializer}
        )
    def get(self, request):
        user = request.user
        PIC = User.objects.filter(id=user.id).first()
        srtp_pro = SRTPProject.objects.filter(person_in_charge=PIC).first()
        if srtp_pro is None:
            return self.success("There is no project")
        else:
            return self.success(srtp_pro.toDict())


class FileUploadAPI(APIView):
    permissions = [student_required, teacher_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: 上传文件",
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
        operation_description="API: 更新SRTP项目信息",
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


'''---------------------------教改项目部分---------------------------------------'''


class EduProjectCreationAPI(APIView):
    permission_classes = [teacher_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: Education  project creation",
        request_body=EduProjectCreationSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = EduProjectCreationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data
            user = request.user
            PIC = User.objects.filter(id=user.id).first()
            edu_project = EduProject.objects.create(pro_level=data["pro_level"],
                                                    person_in_charge=PIC,
                                                    members=data["members"],
                                                    apply_file=data['file_url'],
                                                    pro_name=data['pro_name'],
                                                    introduction=data['introduction'],
                                                    create_year=data['create_year'],
                                                    end_year=data['end_year'])
            edu_project.save()
            return self.success(edu_project.toDict())
        else:
            return self.invalid_serializer(serializer)


class EduUpdateAPI(APIView):
    permissions = [teacher_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: 更新Education项目信息",
        request_body=EduUpdateSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = EduUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data
            edu_pro = EduProject.objects.filter(id=data['pro_id']).first()
            members = data['members']
            introduction = data['introduction']
            file_url = data['file_url']
            if members:
                edu_pro.members = members
            if introduction:
                edu_pro.introduction = introduction
            operation = data['op_code']
            if operation == OperationCode.UPLOAD_INT:
                edu_pro.apply_file = file_url
                edu_pro.pro_state = ProState.UNCONFIRMED
            elif operation == OperationCode.UPLOAD_MID:
                edu_pro.middle_file = file_url
                edu_pro.pro_state = ProState.MIDTERM_CHECKING
            elif operation == OperationCode.UPLOAD_FIN:
                edu_pro.end_file = file_url
                edu_pro.pro_state = ProState.FINAL_CHEKING
            elif operation == OperationCode.UPLOAD_TER:
                edu_pro.abnormal_file = file_url
                edu_pro.pro_state = ProState.TERMINATED
            elif operation == OperationCode.UPLOAD_POS:
                edu_pro.abnormal_file = file_url
                edu_pro.pro_state = ProState.POSTPONED
            edu_pro.save()

            return self.success(edu_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


class EduGetSelfAPI(APIView):
    permission_classes = [teacher_required]

    @swagger_auto_schema(
            operation_description="API: 得到自己管理的项目的详细信息",
            responses={200: SuccessResponseSerializer,
                       400: ErrorResponseSerializer}
        )
    def get(self, request):
        user = request.user
        PIC = User.objects.filter(id=user.id).first()
        edu_pro = EduProject.objects.filter(person_in_charge=PIC).first()
        if edu_pro is None:
            return self.success("There is no project")
        else:
            return self.success(edu_pro.toDict())


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
        serializer = GraProjectCreationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.data
            # user = request.user
            student = User.objects.filter(username=data['student_username']).first()
            teacher = User.objects.filter(username=data['teacher_username']).first()

            gra_project = GraProject.objects.create(pro_level=data["pro_level"],
                                                    pro_state=ProState.UNCONFIRMED,
                                                    teacher=teacher,
                                                    select_file=data['select_file'],
                                                    student=student,
                                                    pro_name=data['pro_name'])
            gra_project.save()
            return self.success(gra_project.toDict())
        else:
            return self.invalid_serializer(serializer)


class GraUpdateAPI(APIView):
    permissions = [student_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: 创建毕设项目",
        request_body=GraUpdateSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = GraUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            gra_pro = GraProject.objects.filter(id=data['pro_id'])
            op_code = data['op_code']
            if op_code == OperationCode.UPLOAD_INT:
                gra_pro.pro_state = ProState.UNCONFIRMED
            elif op_code == OperationCode.UPLOAD_MID:
                gra_pro.pro_state = ProState.MIDTERM_CHECKING
            elif op_code == OperationCode.UPLOAD_FIN:
                gra_pro.pro_state = ProState.FINAL_CHEKING
            gra_pro.save()
            return self.success(gra_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


#  class GraFindSelf


class GraGetSelfAPI(APIView):
    permissions = [student_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: 找到自己的毕设项目",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        user = request.user
        print(user)
        student = User.objects.get(id=user.id)
        print(student)
        gra_pro = GraProject.objects.filter(student=student)
        return self.success(gra_pro.toDict())


#  class GraFindALL

class GraStateChangeAPI(APIView):
    permissions = [teacher_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: 教师发布文件",
        request_body=GraStateChangeSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = GraStateChangeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            gra_pro = GraProject.objects.filter(id=data['pro_id'])
            op_code = data['op_code']
            if op_code == OperationCode.UPLOAD_TASK:
                gra_pro.pro_state = ProState.MIDTERM
            elif op_code == OperationCode.UPLOAD_CHECK:
                gra_pro.pro_state = ProState.FINALTERM
            gra_pro.save()
            return self.success(gra_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


class GraGetAllAPI(APIView):
    permissions = [teacher_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: 找到自己指导的毕设项目",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self, request):
        user = request.user
        teacher = User.objects.get(id=user.id)
        gra_pros = GraProject.objects.filter(teacher=teacher).all()
        total_pro = []
        for gra_pro in gra_pros:
            total_pro.append(gra_pro.toDict())
        return self.success(total_pro)


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
                srtp_pro.pro_state = ProState.MIDTERM
            elif op_code == OperationCode.FIN_PASS:
                srtp_pro.pro_state = ProState.DONE
            elif op_code == OperationCode.MID_PASS:
                srtp_pro.pro_state = ProState.FINALTERM
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


class SRTPFindAllSimpleAPI(APIView):
    permissions = [secretary_required]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self):
        srtp_pros = SRTPProject.objects.all()
        if srtp_pros is None:
            return self.success("no project exist!")
        single_pro = []
        total_pro = []
        for srtp_pro in srtp_pros:
            single_pro.append((srtp_pro.person_in_charge.username, str(getattr(srtp_pro, srtp_pros.person_in_charge.username))))
            single_pro.append((srtp_pro.create_year, str(getattr(srtp_pro, srtp_pros.create_year))))
            single_pro.append((srtp_pro.end_year, str(getattr(srtp_pro, srtp_pros.end_year))))
            single_pro.append((srtp_pro.pro_level, str(getattr(srtp_pro, srtp_pros.pro_level))))
            single_pro.append((srtp_pro.members, str(getattr(srtp_pro, srtp_pros.members))))
            single_pro.append((srtp_pro.pro_name, str(getattr(srtp_pro, srtp_pros.pro_name))))
            single_pro.append((srtp_pro.introduction, str(getattr(srtp_pro, srtp_pros.introduction))))
            single_pro.append((srtp_pro.instructor, str(getattr(srtp_pro, srtp_pros.instructor))))
            total_pro.append(dict(single_pro))
            single_pro = []
        return self.success(total_pro)


class SRTPFindAllAPI(APIView):
    permissions = [secretary_required]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self):
        srtp_pros = SRTPProject.objects.all()
        if srtp_pros is None:
            return self.success("no project exist!")
        total_pro = []
        for srtp_pro in srtp_pros:
            total_pro.append(srtp_pro.toDict())
        return self.success(total_pro)


class SRTPGetAllAPI(APIView):
    permissions = [secretary_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        request_body=SRTPGetALLSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPGetALLSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.get(id=data['pro_id'])
            return self.success(srtp_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


class EduStateChangeAPI(APIView):
    permissions = [secretary_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        request_body=EduStateChangeSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = EduStateChangeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            edu_pro = EduProject.objects.filter(id=data['pro_id']).first()
            op_code = data['op_code']
            if op_code == OperationCode.CREATION_PASS:
                edu_pro.pro_state = ProState.MIDTERM
            elif op_code == OperationCode.FIN_PASS:
                edu_pro.pro_state = ProState.DONE
            elif op_code == OperationCode.MID_PASS:
                edu_pro.pro_state = ProState.FINALTERM
            elif op_code == OperationCode.REJECT:
                edu_pro.pro_state = ProState.TERMINATED
                edu_pro.save()
            return self.success(edu_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


class EduLevelChangeAPI(APIView):
    permissions = [secretary_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        request_body=EduLevelChangeSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = EduLevelChangeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            edu_pro = EduProject.objects.filter(id=data['pro_id']).first()
            edu_pro.pro_level = data['pro_level']
            edu_pro.save()
            return self.success(edu_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


class EduFindAllAPI(APIView):
    permissions = [secretary_required]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def get(self):
        edu_pros = EduProject.objects.all()
        if edu_pros is None:
            return self.success("no project exist!")
        total_pro = []
        for edu_pro in edu_pros:
            total_pro.append(edu_pro.toDict())
        return self.success(total_pro)


class EduGetAllAPI(APIView):
    permissions = [secretary_required]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="API: SRTP project state change",
        request_body=SRTPGetALLSerializer,
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = SRTPGetALLSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            srtp_pro = SRTPProject.objects.get(id=data['pro_id'])
            return self.success(srtp_pro.toDict())
        else:
            return self.invalid_serializer(serializer)


