from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from . import models
from . import permissions
from . import serializers


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


class PupilViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PupilSerializer
    queryset = models.Pupil.objects.all()
    permission_classes = [permissions.IsSuperuserOrReadOnly]


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()
    permission_classes = [permissions.IsSuperuser]

    def list(self, request, *args, **kwargs):
        group_id = self.request.query_params.get('group_id')
        pupil_id = self.request.query_params.get('pupil_id')
        date = self.request.query_params.get('date')

        if date and len(date.split('-')[0]) != 4:
            return Response(data={'detail': 'Date is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        if group_id:
            self.queryset = self.queryset.filter(group__id=group_id)

        if pupil_id:
            self.queryset = self.queryset.filter(pupil__id=pupil_id)

        if date:
            try:
                if len(date.split('-')) == 3:
                    self.queryset = self.queryset.filter(date=date)
                elif len(date.split('-')) == 2:
                    self.queryset = self.queryset.filter(date__year=date.split('-')[0], date__month=date.split('-')[1])
                elif len(date.split('-')) == 1:
                    self.queryset = self.queryset.filter(date__year=date.split('-')[0])
                else:
                    return Response(data={'detail': 'Date is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={'detail': 'Date is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(self.queryset, many=True)

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
