# Generated by Django 3.1.4 on 2021-02-07 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20210207_1357'),
        ('impressao', '0005_auto_20210204_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impressao',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.usuario'),
        ),
    ]