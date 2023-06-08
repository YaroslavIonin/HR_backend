from django.contrib import admin
from .models import User, Department, Bid
from back.models import Resume


class DepartmentInstanceInline(admin.StackedInline):
    model = User
    fields = ('full_name', 'email')
    extra = 0


class ResumeInstanceInline(admin.StackedInline):
    model = Resume
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'is_admin', 'is_header_dep']
    fields = (('full_name', 'email', 'phone_number'), 'password', 'image', ('is_admin', 'is_header_dep', 'is_active'),
              'department')
    empty_value_display = '-empty-'
    list_filter = ('full_name', 'email', 'is_admin', 'is_header_dep')
    list_max_show_all = 20
    # readonly_fields = ('password',)
    list_per_page = 10
    search_fields = ['email', 'full_name']
    search_help_text = 'Поиск осуществляется по email и full_name пользователей'
    inlines = [ResumeInstanceInline]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ('name', 'description', 'count')
    empty_value_display = '-empty-'
    list_filter = ('name',)
    list_max_show_all = 20
    list_per_page = 10
    search_fields = ['name']
    search_help_text = 'Поиск осуществляется по названию департамента'
    inlines = [DepartmentInstanceInline]


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['addressee', 'destination', 'status']
    list_filter = ('status',)
    list_max_show_all = 20
    list_per_page = 10
    search_fields = ['addressee', 'destination']
    # search_help_text = 'Поиск осуществляется по названию департамента'
