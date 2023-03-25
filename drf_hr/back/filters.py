from django_filters import rest_framework as filters

from back.models import Vacancy, Resume


class VacancyFilter(filters.FilterSet):
    class Meta:
        model = Vacancy
        fields = {
            'exp_work': ['gte'],
            'salary': ['gte'],
            'department': ['exact'],
        }


class ResumeFilter(filters.FilterSet):
    class Meta:
        model = Resume
        fields = {
            'exp_work': ['gte'],
            'salary': ['gte'],
        }
