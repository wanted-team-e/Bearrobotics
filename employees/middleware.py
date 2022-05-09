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
        try:
            if (
                request.path != "/api/users/signup"
                and request.path != "/api/users/login"
                and "admin" not in request.path
                and "swagger" not in request.path
            ):

                headers = request.headers
                access_token = headers.get("Authorization", None)
                print(access_token)
                if not access_token:
                    raise PermissionDenied()

                payload = decode_jwt(access_token)
                email = payload.get("email", None)

                if not email:
                    raise PermissionDenied()
                Employee.objects.get(email=email)
            response = self.get_response(request)

            return response

        except (PermissionDenied, Employee.DoesNotExist):
            return JsonResponse(
                {"error": "Authorization Error"}, status=status.HTTP_401_UNAUTHORIZED
            )

        except ExpiredSignatureError:
            return JsonResponse(
                {"error": "Expired token. Please log in again."},
                status=status.HTTP_403_FORBIDDEN,
            )