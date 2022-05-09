from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from employees.jwt import generate_access_token
from employees.models import Employee
from employees.permissions import EmployeePermission
from employees.serializers import EmployeeSerializer, UserSignupSerializer, UserLoginSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin, GenericViewSet):
    queryset = Employee.objects.all()


    def get_permissions(self):
        permission_classes = []
        if self.action in ('signup', 'login', 'retrieve', 'list'):
            permission_classes = (AllowAny,)
        else:
            permission_classes = (EmployeePermission,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in 'signup':
            return UserSignupSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        else:
            return EmployeeSerializer

    @swagger_auto_schema(
        operation_description='유저 수정 api 입니다.',
        operation_summary='user update api'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='유저 삭제 api 입니다.',
        operation_summary='user delete api'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='유저 상세보기 api 입니다.',
        operation_summary='user retrieve api'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='유저 리스트 보기 api 입니다.',
        operation_summary='user list api'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='유저 로그인 api 입니다.',
        operation_summary='user login api'
    )
    @action(methods=['post'], detail=False)
    def login(self, request):
        data = {}
        employee = self.get_serializer().validate(request.data)
        if employee is None:
            return Response({'message': 'Not Valid request data'}, status=status.HTTP_400_BAD_REQUEST)
        data['access_token'] = generate_access_token(employee)
        data['email'] = employee.email
        data['id'] = employee.id
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='유저 회원가입 api 입니다.',
        operation_summary='user signup(create) api'
    )
    @action(methods=['post'], detail=False)
    def signup(self, request):
        data = {}
        serializer = UserSignupSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Request Body Error.'}, status=status.HTTP_400_BAD_REQUEST)
        if Employee.objects.filter(email=serializer.validated_data['email']).first() is None:
            user = serializer.save()
            employee = user
            data['access_token'] = generate_access_token(employee)
            data['email'] = employee.email
            data['id'] = employee.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({'message': 'duplicate email'}, status=status.HTTP_409_CONFLICT)
