from django.shortcuts import render
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail


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
