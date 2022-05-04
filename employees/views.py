from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from employees.jwt import generate_access_token
from employees.models import Employee
from employees.serializers import AuthenticationSerializer, EmployeeSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin, GenericViewSet):
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        if self.action == ['signup','login']:
            return AuthenticationSerializer
        else:
            return EmployeeSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer.create(serializer.data)
        return Response({'message': 'Signup Succeed'},status =status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        employee = self.get_serializer().validate(request.data)
        if employee is None:
            return Response(status=400)
        token = generate_access_token(employee)
        return Response(token, status=200)