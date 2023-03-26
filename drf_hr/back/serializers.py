from rest_framework import serializers
from .models import Resume, Vacancy, Skills


class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    data_updated = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'email': obj.user.email,
        }

    def get_data_updated(self, obj):
        return str(obj.data_updated).split('T')[0].split(' ')[0]

    class Meta:
        model = Resume
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    department = serializers.SerializerMethodField(read_only=True)
    data_updated = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'email': obj.user.email,
        }

    def get_data_updated(self, obj):
        return str(obj.data_updated).split('T')[0].split(' ')[0]

    def get_department(self, obj):
        return str(obj.department)

    class Meta:
        model = Vacancy
        fields = '__all__'


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'