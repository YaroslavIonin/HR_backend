from django.db import models
from django.conf import settings


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор вакансии', on_delete=models.CASCADE)
    exp_work = models.IntegerField(verbose_name='Стаж работы')
    salary = models.IntegerField(verbose_name='Желаемая заработная плата')
    about_me = models.TextField(max_length=500, verbose_name='О сотруднике')
    TO_WORK = 'T_W'
    NOT_PUBLISHED = 'N_P'
    YES_PUBLISHED = 'Y_P'
    statuses = [
        (TO_WORK, 'TO_WORK'),
        (NOT_PUBLISHED, 'NOT_PUBLISHED'),
        (YES_PUBLISHED, 'YES_PUBLISHED')
    ]
    status = models.CharField(max_length=3, choices=statuses, default=TO_WORK)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
