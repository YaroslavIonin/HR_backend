from rest_framework import serializers
from .models import Department, User
from django.contrib.auth import get_user_model


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)
    is_header_dep = serializers.SerializerMethodField(read_only=True)

    def get_is_admin(self, obj):
        return obj.is_admin

    def get_is_header_dep(self, obj):
        return obj.is_header_dep

    def get_department(self, obj):
        return str(obj.department)

    class Meta:
        model = get_user_model()
        queryset = User.objects.all()
        fields = ['id', 'email', 'full_name', 'is_admin', 'is_header_dep', 'department', 'image', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(email=validated_data['email'], full_name=validated_data['full_name'])
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)
