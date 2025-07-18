# Generated by Django 5.2.4 on 2025-07-13 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlatoTipico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Plato')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('region', models.CharField(blank=True, max_length=50, null=True, verbose_name='Región')),
                ('ingredientes_principales', models.CharField(max_length=200, verbose_name='Ingredientes Principales')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='platos/', verbose_name='Imagen')),
            ],
            options={
                'verbose_name': 'Plato Típico de Ecuador',
                'verbose_name_plural': 'Platos Típicos de Ecuador',
                'ordering': ['nombre'],
            },
        ),
    ]
