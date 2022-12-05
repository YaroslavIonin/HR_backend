from rest_framework import serializers
from .models import Resume, Vacancy


class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'email': obj.user.email,
        }

    class Meta:
        model = Resume
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    department = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'email': obj.user.email,
        }

    def get_department(self, obj):
        return str(obj.department)

    class Meta:
        model = Vacancy
        fields = '__all__'