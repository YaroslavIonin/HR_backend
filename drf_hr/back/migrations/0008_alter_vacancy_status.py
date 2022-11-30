# Generated by Django 4.1.2 on 2022-11-01 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0007_alter_vacancy_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='status',
            field=models.CharField(choices=[('T_W', 'В работе'), ('N_P', 'Не опубликовано'), ('Y_P', 'Опубликовано')], default='T_W', max_length=3, verbose_name='Статус вакансии:'),
        ),
    ]
