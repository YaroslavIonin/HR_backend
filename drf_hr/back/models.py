import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.conf import settings
from accounts.models import Department, User


class Skills(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название навыка')
    statuses_skills = [
        (1, 'hard skill'),
        (0, 'soft skill')
    ]
    status = models.IntegerField(choices=statuses_skills, verbose_name='Вид навыка')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['name']


class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Автор резюме', on_delete=models.CASCADE)
    exp_work = models.PositiveSmallIntegerField(verbose_name='Стаж работы', default=0)
    salary = models.PositiveIntegerField(verbose_name='Желаемая заработная плата', default=0)
    about_me = models.TextField(max_length=1500, verbose_name='О сотруднике', blank=True, null=True)
    status = models.IntegerField(choices=[
        (0, 'Не опубликовано'),
        (1, 'Опубликовано')
    ], default=0, verbose_name='Статус резюме:')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фото', blank=True, null=True)
    data_updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    file = models.FileField(upload_to='files/%Y/%m/%d/', verbose_name='Файл с резюме', blank=True, null=True)

    def __str__(self):
        return f'Резюме: {self.user}'

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-data_updated']


class Vacancy(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название вакансии')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор вакансии', on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=1500, verbose_name='Описание вакансии', blank=True, null=True)
    exp_work = models.PositiveSmallIntegerField(verbose_name='Требуемый стаж работы', default=0)
    salary = models.PositiveIntegerField(verbose_name='Заработная плата', default=0)
    department = models.ForeignKey(Department, blank=True, null=True, verbose_name='Департамент', on_delete=models.RESTRICT)
    status = models.IntegerField(choices=[
        (0, 'Не опубликовано'),
        (1, 'Опубликовано')
    ], default=0, verbose_name='Статус вакансии:')
    data_updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования/публикации')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_vacancies', default=[], blank=[])
    skills = models.ManyToManyField(Skills, related_name='skills', default=[], blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.department = User.objects.get(id=self.user.id).department
        super(Vacancy, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-data_updated']
