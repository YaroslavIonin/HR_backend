from django.shortcuts import render
from .models import User, Department
from .serializers import UserSerializer, DepartmentSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
