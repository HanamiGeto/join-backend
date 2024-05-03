from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth.models import User

class EmailAuthentication(BaseAuthentication):
    def authenticate(self, request):
        email = request.data.get('email') 
        password = request.data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                return (user, None)
            else:
                raise AuthenticationFailed("Unable to log in with provided credentials.")
        else:
            raise AuthenticationFailed("Must include 'email' and 'password'.")
