
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from employees.jwt import generate_access_token
from employees.models import Employee
from employees.serializers import EmployeeSerializer, UserSignupSerializer, UserLoginSerializer


class UserViewSet(mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin, GenericViewSet):

    def get_queryset(self):
        if self.action == 'list':
            return Employee.objects.all().order_by('-group')
        else:
            return Employee.objects.all()


    def get_serializer_class(self):
        if self.action in 'signup':
            return UserSignupSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        else:
            return EmployeeSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        data = {}
        employee = self.get_serializer().validate(request.data)
        if employee is None:
            return Response({'message':'Not Valid request data'}, status=status.HTTP_400_BAD_REQUEST)
        data['access_token'] = generate_access_token(employee)
        data['email'] = employee.email
        data['id'] = employee.id
        return Response(data, status=status.HTTP_200_OK)

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