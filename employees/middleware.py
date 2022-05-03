from jwt import ExpiredSignatureError
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS
from .models import Employee
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .jwt import decode_jwt

class JsonWebTokenMiddleWare(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pass