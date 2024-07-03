from rest_framework import serializers
from .models import Patient
from django.contrib.auth.models import User


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Patient
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email',
                  'first_name', 'last_name', 'confirm_password', 'password']

    def save(self, **kwargs):
        username = self.validated_data['username']
        email = self.validated_data['email']
        last_name = self.validated_data['last_name']
        first_name = self.validated_data['first_name']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']

        if password != password2:
            raise serializers.ValidationError(
                {'error': "Passwords do not match"})

        if User.objects.filter(username=username, email=email).exists():
            raise serializers.ValidationError(
                {'error': 'This email already exists'})

        account = User(username=username, email=email,
                       last_name=last_name, first_name=first_name)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
