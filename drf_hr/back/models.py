from django.db import models
from django.conf import settings


class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Автор резюме', on_delete=models.CASCADE)
    exp_work = models.IntegerField(verbose_name='Стаж работы', default=0)
    salary = models.IntegerField(verbose_name='Желаемая заработная плата', default=0)
    about_me = models.TextField(max_length=500, verbose_name='О сотруднике', blank=True, null=True)
    TO_WORK = 'T_W'
    NOT_PUBLISHED = 'N_P'
    YES_PUBLISHED = 'Y_P'
    statuses = [
        (TO_WORK, 'В работе'),
        (NOT_PUBLISHED, 'Не опубликовано'),
        (YES_PUBLISHED, 'Опубликовано')
    ]
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
