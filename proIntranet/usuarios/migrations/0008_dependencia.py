# Generated by Django 2.2.4 on 2019-10-17 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_perfil_cargo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacion', models.CharField(max_length=100, unique=True)),
                ('sede', models.CharField(choices=[('CEN', 'CENTRAL'), ('VTA', 'VILLETA'), ('VMI', 'VALLEMI')], default='CEN', max_length=3)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
