# Generated by Django 3.1.4 on 2021-02-01 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0002_auto_20210128_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoImpressao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=55, verbose_name='nome')),
                ('descricao', models.CharField(blank=True, max_length=255, null=True, verbose_name='descricao')),
            ],
        ),
        migrations.CreateModel(
            name='Impressao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=55, null=True, verbose_name='comentario')),
                ('uri_arquivo', models.FileField(upload_to='')),
                ('qtd_copias', models.SmallIntegerField(verbose_name='qtd_copias')),
                ('visualizado_em', models.DateTimeField(blank=True, null=True, verbose_name='visualizado_em')),
                ('prazo_entrega', models.DateTimeField(blank=True, null=True, verbose_name='prazo_entrega')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.usuario')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='impressao.tipoimpressao')),
            ],
        ),
    ]
