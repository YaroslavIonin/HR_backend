from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'is_admin', 'is_header_dep']
    fields = (('full_name', 'email'), 'password', 'image', ('is_admin', 'is_header_dep'), 'department')
    empty_value_display = '-empty-'
    list_filter = ('full_name', 'email', 'is_admin', 'is_header_dep')
    list_max_show_all = 20
    readonly_fields = ('password',)
    list_per_page = 10
    search_fields = ['email', 'full_name']
    search_help_text = 'Поиск осуществляется по email и full_name пользователей'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ('name', 'description')
    empty_value_display = '-empty-'
    list_filter = ('name',)
    list_max_show_all = 20
    list_per_page = 10
    search_fields = ['name']
    search_help_text = 'Поиск осуществляется по названию департамента'


