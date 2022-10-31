from rest_framework import serializers
from .models import Resume, Vacancy


class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return str(obj.user.id)

    class Meta:
        model = Resume
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    department = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return str(obj.user.id)

    def get_department(self, obj):
        return str(obj.department)

    class Meta:
        model = Vacancy
        fields = '__all__'