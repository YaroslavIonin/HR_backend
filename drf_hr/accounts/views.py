from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .models import User, Department
from .serializers import UserSerializer, DepartmentSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticated,)


class UserViewSet(ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)
