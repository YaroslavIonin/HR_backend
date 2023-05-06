from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Resume, Vacancy, Skills


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'exp_work', 'salary', 'status', 'data_updated']
    fields = (('user', 'status'), ('exp_work', 'salary'), 'about_me', 'image', 'file', 'skills')
    empty_value_display = '-empty-'
    # readonly_fields = ('user', 'exp_work', 'salary', 'status', 'data_updated' )
    list_filter = ('user', 'exp_work', 'salary', 'status', 'data_updated')
    list_max_show_all = 20
    list_per_page = 10
    search_fields = ['user']
    search_help_text = 'Поиск осуществляется по ФИО пользователей'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'department', 'status']
    fields = (
        ('title', 'status'),
        ('user', 'department'),
        ('employment', 'schedule'),
        ('exp_work', 'salary_from', 'salary_to'),
        'description',
        'skills')
    empty_value_display = '-empty-'
    readonly_fields = ('department',)
    list_filter = (
        'title', 'user', 'department', 'employment', 'exp_work', 'salary_from', 'salary_to', 'schedule', 'status')
    list_max_show_all = 20
    list_per_page = 10
    search_fields = ['user', 'title', 'department', 'status']
    search_help_text = 'Поиск осуществляется по ФИО пользователей, департаменту и названию или статусу вакансии'


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
