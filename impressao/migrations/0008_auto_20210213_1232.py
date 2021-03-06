# Generated by Django 3.1.4 on 2021-02-13 15:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impressao', '0007_auto_20210208_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='impressao',
            name='data_pedido',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 2, 13, 12, 32, 35, 894989), verbose_name='data_pedido'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impressao',
            name='qtd_laudas_imprimidas',
            field=models.IntegerField(blank=True, null=True, verbose_name='qtd_laudas_imprimidas'),
        ),
        migrations.AddField(
            model_name='impressao',
            name='set_imprimida_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='set_imprimida_em'),
        ),
    ]
