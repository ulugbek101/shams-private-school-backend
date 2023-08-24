from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from . import models
from . import permissions
from . import serializers


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsSuperuserOrReadOnly]

    def get_queryset(self):
        return models.Subject.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsSuperuserOrReadOnly]

    def get_queryset(self):
        return get_user_model().objects.all()

    def list(self, request, *args, **kwargs):
        name = self.request.query_params.get('name')

        queryset = self.get_queryset()

        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name)
            )

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsSuperuserOrIsOwner]

    def get_queryset(self):
        return models.Group.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        teacher = self.request.query_params.get('teacher')
        name = self.request.query_params.get('name')

        if teacher:
            queryset = queryset.filter(teacher__id=teacher)

        if name:
            queryset = queryset.filter(name__icontains=name)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


class PupilViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PupilSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsSuperuserOrReadOnly]

    def get_queryset(self):
        return models.Pupil.objects.all()


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsSuperuser]

    def get_queryset(self):
        return models.Payment.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        group_id = self.request.query_params.get('group_id')
        pupil_id = self.request.query_params.get('pupil_id')
        date = self.request.query_params.get('date')

        if date and len(date.split('-')[0]) != 4:
            return Response(data={'detail': 'Date is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        if group_id:
            queryset = queryset.filter(group__id=group_id)

        if pupil_id:
            queryset = queryset.filter(pupil__id=pupil_id)

        if date:
            try:
                if len(date.split('-')) == 3:
                    queryset = queryset.filter(date=date)
                elif len(date.split('-')) == 2:
                    queryset = queryset.filter(date__year=date.split('-')[0], date__month=date.split('-')[1])
                elif len(date.split('-')) == 1:
                    queryset = queryset.filter(date__year=date.split('-')[0])
                else:
                    return Response(data={'detail': 'Date is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={'detail': 'Date is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     group_id = self.request.query_params.get('group_id')
    #     pupil_id = self.request.query_params.get('pupil_id')
    #     date = self.request.query_params.get('date')
    #
    #     if date and len(date.split('-')[0]) != 4:
    #         return Response(data={'detail': 'Date is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     if group_id:
    #         self.queryset = self.queryset.filter(group__id=group_id)
    #
    #     if pupil_id:
    #         self.queryset = self.queryset.filter(pupil__id=pupil_id)
    #
    #     if date:
    #         self.queryset = self.queryset.filter(date__year=date.split('-')[1], date__month=date.split('-')[0])
    #
    #     serializer = self.serializer_class(self.get_object(), many=False)
    #
    #     return Response(serializer.data)
