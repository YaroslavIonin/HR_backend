import datetime

from django.db import models
from django.conf import settings
from accounts.models import Department, User

TO_WORK = 'T_W'
NOT_PUBLISHED = 'N_P'
YES_PUBLISHED = 'Y_P'
statuses = [
    (TO_WORK, 'В работе'),
    (NOT_PUBLISHED, 'Не опубликовано'),
    (YES_PUBLISHED, 'Опубликовано')
]


class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Автор резюме', on_delete=models.CASCADE)
    exp_work = models.PositiveSmallIntegerField(verbose_name='Стаж работы', default=0)
    salary = models.PositiveIntegerField(verbose_name='Желаемая заработная плата', default=0)
    about_me = models.TextField(max_length=500, verbose_name='О сотруднике', blank=True, null=True)
    status = models.CharField(max_length=3, choices=statuses, default=TO_WORK, verbose_name='Статус резюме:')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фото', blank=True, null=True)
    data_updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    file = models.FileField(upload_to='files/%Y/%m/%d/', verbose_name='Файл с резюме', blank=True, null=True)

    def __str__(self):
        return 'Резюме: {}'.format(self.user)

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-data_updated']


class Vacancy(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название вакансии')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор вакансии', on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=500, verbose_name='Описание вакансии', blank=True, null=True)
    exp_work = models.PositiveSmallIntegerField(verbose_name='Требуемый стаж работы', default=0)
    salary = models.PositiveIntegerField(verbose_name='Заработная плата', default=0)
    department = models.ForeignKey(Department, blank=True, null=True, verbose_name='Департамент', on_delete=models.RESTRICT)
    status = models.CharField(max_length=3, choices=statuses, default=TO_WORK, verbose_name='Статус вакансии:')
    data_updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования/публикации')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.department = User.objects.get(id=self.user.id).department
        super(Vacancy, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-data_updated']
