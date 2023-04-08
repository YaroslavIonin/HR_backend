from django_filters import rest_framework as filters, NumberFilter, ModelMultipleChoiceFilter

from back.models import Vacancy, Resume, Skills


class VacancyFilter(filters.FilterSet):
    exp_work__gt = NumberFilter(field_name='exp_work', lookup_expr='gte')
    exp_work__lt = NumberFilter(field_name='exp_work', lookup_expr='lte')

    salary__gt = NumberFilter(field_name='salary', lookup_expr='gte')
    salary__lt = NumberFilter(field_name='salary', lookup_expr='lte')

    skills = ModelMultipleChoiceFilter(
        field_name='skills',
        queryset=Skills.objects.all(),
    )

    class Meta:
        model = Vacancy
        fields = {
            'department': ['exact'],
        }


class ResumeFilter(filters.FilterSet):
    exp_work__gt = NumberFilter(field_name='exp_work', lookup_expr='gte')
    exp_work__lt = NumberFilter(field_name='exp_work', lookup_expr='lte')
    salary__gt = NumberFilter(field_name='salary', lookup_expr='gte')
    salary__lt = NumberFilter(field_name='salary', lookup_expr='lte')

    class Meta:
        model = Resume
        fields = {}

