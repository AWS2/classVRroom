# Generated by Django 3.2 on 2023-05-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vroom', '0006_auto_20220929_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='archivo',
            field=models.FileField(blank=True, default=None, null=True, upload_to='performances/'),
        ),
    ]
