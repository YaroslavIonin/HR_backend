# Generated by Django 4.1.2 on 2022-11-30 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='addressee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL, verbose_name='От кого'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата редактирования'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кому(поле id)'),
        ),
    ]