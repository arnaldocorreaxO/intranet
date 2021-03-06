# Generated by Django 2.2.4 on 2019-11-01 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0021_auto_20191031_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='ciudad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bs.Ciudad'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bs.Departamento'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='genero',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, null=True),
        ),
    ]
