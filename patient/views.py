from django.shortcuts import redirect
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer, UserSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class UserRegistrationAPIview(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            print("Token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("uid ", uid)

            confirmation_link = f"http://127.0.0.1:8000/patients/active/{uid}/{token}/"

            message = f"Your account activation link: {confirmation_link}"

            send_mail("Account activation link", message,
                      "noreply@gmail.com", [user.email])

            return Response({'details': 'Please check your email for registration'})
        return Response(serializer.errors)


def activate_account(request, uuid64, token):
    try:
        uid = urlsafe_base64_decode(uuid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("register")
    else:
        return redirect("register")


class UserLoginAPIview(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user=user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'errors': "No users exist with given credentials"})
        return Response(serializer.errors)


class UserLogoutAPIview(APIView):
    def get(self, request, *args):
        request.user.auth_token.delete()
        logout(request)
        return redirect("login")
