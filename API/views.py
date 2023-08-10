from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from . import models


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubjectSerializer
    queryset = models.Subject.objects.all()
