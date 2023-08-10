from django.db.models import Q
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

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

    def list(self, request, *args, **kwargs):
        name = self.request.query_params.get('name')

        if name:
            self.queryset = self.queryset.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name)
            )

        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [permissions.IsSuperuserOrIsOwner]

    def list(self, request, *args, **kwargs):
        teacher = self.request.query_params.get('teacher')
        name = self.request.query_params.get('name')

        if teacher:
            self.queryset = self.queryset.filter(teacher__id=teacher)

        if name:
            self.queryset = self.queryset.filter(name__icontains=name)

        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)
