# Generated by Django 3.2 on 2022-04-01 16:07

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Auto_Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passed_items', models.IntegerField(default=0)),
                ('failed_items', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('comments', models.CharField(blank=True, default=None, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('icono', models.ImageField(blank=True, default=None, null=True, upload_to='')),
                ('administrador', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('estado', models.BooleanField(default=False)),
                ('centro', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.centro')),
            ],
        ),
        migrations.CreateModel(
            name='Ejercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, default=None, null=True)),
                ('enunciado', models.TextField()),
                ('nota_maxima', models.FloatField()),
                ('fecha_publicacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('min_exercise_version', models.FloatField(blank=True, default=1.0, null=True)),
                ('autor', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Termino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.FloatField()),
                ('permisos', models.IntegerField()),
                ('texto', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Ejercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Subscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vroom.curso')),
                ('tipo_subscripcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vroom.tipo_subscripcion')),
                ('usuario', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Texto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('texto', models.TextField(null=True)),
                ('fecha_publicacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('autor', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(default=None, max_length=4, unique=True)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.ejercicio')),
                ('usuario', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('fecha_publicacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('autor', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vroom.curso')),
                ('tipo_subscripcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vroom.tipo_subscripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_publicacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_edicion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_calificacion', models.DateTimeField(blank=True, default=None, null=True)),
                ('archivo', models.FileField(blank=True, default=None, null=True, upload_to='static/assets/archivos')),
                ('comentario_alumno', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('comentario_profesor', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('nota', models.FloatField(blank=True, default=True, null=True)),
                ('autor', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.ejercicio')),
                ('profesor', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profesor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='tipo_ejercicio',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.tipo_ejercicio'),
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('archivo', models.FileField(null=True, upload_to='documents/')),
                ('fecha_publicacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('autor', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(default=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.curso')),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='termino',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vroom.termino'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
