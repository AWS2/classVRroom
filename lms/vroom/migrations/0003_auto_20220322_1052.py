# Generated by Django 3.2 on 2022-03-22 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vroom', '0002_auto_20220315_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipo_ejercicio',
            name='icono',
            field=models.ImageField(upload_to='static/assets/archivos'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
