# Generated by Django 3.1.4 on 2021-02-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impressao', '0010_auto_20210213_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(max_length=255, unique=True, verbose_name='nome'),
        ),
    ]
