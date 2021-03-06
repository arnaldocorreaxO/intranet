# Generated by Django 2.2.4 on 2019-11-01 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0023_auto_20191101_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rh.Cargo'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bs.Departamento'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='dependencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rh.Dependencia'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nacionalidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bs.Nacionalidad'),
        ),
    ]
