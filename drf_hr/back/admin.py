from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'exp_work', 'salary', 'status', 'data_updated']
    fields = (('user', 'status'), ('exp_work', 'salary'), 'about_me', 'image', 'file')
    empty_value_display = '-empty-'
    # readonly_fields = ('user', 'exp_work', 'salary', 'status', 'data_updated' )
    list_filter = ('user', 'exp_work', 'salary', 'status', 'data_updated')
    list_max_show_all = 20
    list_per_page = 10
    search_fields = ['user']
    search_help_text = 'Поиск осуществляется по ФИО пользователей'
