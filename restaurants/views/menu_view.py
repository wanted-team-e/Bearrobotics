from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from restaurants.models import Menu
from restaurants.serializers import MenuSerializer


class MenuViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @swagger_auto_schema(
        operation_description='그룹별 메뉴 생성 api입니다.',
        operation_summary='menu create api'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='메뉴 수정 api 입니다.',
        operation_summary='menu update api'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='메뉴 삭제 api 입니다.',
        operation_summary='menu delete api'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='메뉴 상세보기 api 입니다.',
        operation_summary='menu retrieve api'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
