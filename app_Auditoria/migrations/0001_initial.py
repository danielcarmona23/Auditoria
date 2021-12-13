# Generated by Django 3.2.8 on 2021-11-25 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('estado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_Genero', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identidad', models.CharField(max_length=100)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_Auditoria.genero')),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnostico', models.CharField(max_length=100)),
                ('tratamiento', models.CharField(max_length=100)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('paciente', models.CharField(max_length=100)),
                ('doctor', models.CharField(max_length=100)),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_Auditoria.cita')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identidad', models.CharField(max_length=100)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=50)),
                ('correo', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_Auditoria.genero')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cita',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_Auditoria.doctor'),
        ),
        migrations.AddField(
            model_name='cita',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_Auditoria.paciente'),
        ),
        migrations.AddField(
            model_name='cita',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Asiganacion_Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_Auditoria.cita')),
            ],
        ),
    ]
