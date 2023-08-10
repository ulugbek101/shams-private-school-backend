from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from . import models
from . import permissions


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubjectSerializer
    queryset = models.Subject.objects.all()
    permission_classes = [permissions.IsSuperuserOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [permissions.IsSuperuserOrReadOnly]
