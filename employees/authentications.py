import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from employees.jwt import decode_jwt
from employees.models import Employee


class JSONWebTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        headers = request.headers
        jwt_value = headers.get("Authorization", None)

        if jwt_value is None:
            return None

        try:
            payload = decode_jwt(jwt_value)

        except jwt.ExpiredSignatureError:
            msg = 'Signature has expired.'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        email = payload['email']
        user = Employee.objects.get(email=email)
        return (user, payload)