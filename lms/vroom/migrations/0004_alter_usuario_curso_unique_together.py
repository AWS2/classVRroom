# Generated by Django 3.2 on 2022-09-24 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vroom', '0003_auto_20220921_1632'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usuario_curso',
            unique_together={('usuario', 'curso', 'tipo_subscripcion')},
        ),
    ]
