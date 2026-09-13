from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets


from users.models import CustomUser
from users.serializers import CustomUserSerializer


# class UserCreateAPIView(CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

class MyUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]





