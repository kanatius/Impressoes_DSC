# Generated by Django 3.1.4 on 2021-02-09 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20210207_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='funcionario_aluno',
            field=models.BooleanField(blank=True, null=True, verbose_name='funcionario_aluno'),
        ),
    ]
