# Generated by Django 3.1.2 on 2021-06-09 04:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210527_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='date',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]
