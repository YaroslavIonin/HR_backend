from django.db.models import QuerySet
from django_filters import rest_framework as filters, NumberFilter, ModelMultipleChoiceFilter, MultipleChoiceFilter

from back.models import Vacancy, Resume, Skills, schedule_choices


class VacancyFilter(filters.FilterSet):
    exp_work__gt = NumberFilter(field_name='exp_work', lookup_expr='gte')
    exp_work__lt = NumberFilter(field_name='exp_work', lookup_expr='lte')

    # salary__gt = NumberFilter(field_name='salary', lookup_expr='gte')
    # salary__lt = NumberFilter(field_name='salary', lookup_expr='lte')
    salary = NumberFilter(method='custom_filter_salary', label='Заработная плата')

    employment = MultipleChoiceFilter(
        choices=[
            (0, 'Проектная работа'),
            (1, 'Стажировка'),
            (2, 'Частичная занятость'),
            (3, 'Полная занятость')
        ]
    )

    schedule = MultipleChoiceFilter(
        choices=schedule_choices,
        method='custom_filter_schedule'
    )

    skills = ModelMultipleChoiceFilter(
        field_name='skills',
        queryset=Skills.objects.all(),
    )

    class Meta:
        model = Vacancy
        fields = {
            'department': ['exact'],
        }

    def custom_filter_salary(self, queryset, name, value):
        return queryset.filter(salary_to__gte=value, salary_from__lte=value)

    def custom_filter_schedule(self, queryset: QuerySet, name, value):
        result = Vacancy.objects.none()

        for item in value:
            result |= queryset.filter(schedule__contains=item)

        return result


class ResumeFilter(filters.FilterSet):
    exp_work__gt = NumberFilter(field_name='exp_work', lookup_expr='gte')
    exp_work__lt = NumberFilter(field_name='exp_work', lookup_expr='lte')

    salary__gt = NumberFilter(field_name='salary', lookup_expr='gte')
    salary__lt = NumberFilter(field_name='salary', lookup_expr='lte')
    # salary = NumberFilter(method='custom_filter_salary', label='Заработная плата')

    skills = ModelMultipleChoiceFilter(
        field_name='skills',
        queryset=Skills.objects.all(),
    )

    # def custom_filter_salary(self, queryset, name, value):
    #     return queryset.filter(salary_to__gte=value, salary_from__lte=value)

    class Meta:
        model = Resume
        fields = {}
