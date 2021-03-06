# Generated by Django 2.2.4 on 2019-10-31 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0020_auto_20191031_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_cargo_empleado_perfil', to='rh.Cargo'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='dependencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_dependencia_empleado_perfil', to='rh.Dependencia'),
        ),
    ]
