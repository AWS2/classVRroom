from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import os, datetime, random


class Usuario(AbstractUser):
    termino = models.ForeignKey('Termino',on_delete=models.DO_NOTHING,null=True)
    centro = models.ForeignKey('Centro',on_delete=models.CASCADE,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username
    @property
    def es_admin(self):
        if self.groups.filter(name='admin centro').exists():
            return True
        return False
    @property
    def es_profesor(self):
        if self.groups.filter(name='profesor').exists():
            return True
        return False
    def __str__(self):
        return "{} {} ({})".format(self.first_name,self.last_name,self.email)
Usuario._meta.get_field('email')._unique = True
Usuario._meta.get_field('email').blank = False
Usuario._meta.get_field('email').null = False


class Termino(models.Model):
    version = models.FloatField()
    permisos = models.IntegerField()
    texto = models.TextField(null=True)
    def __str__(self):
        return self.texto

class Centro(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.ImageField(default=None, blank=True, null=True)
    administrador = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,related_name="admin_centro")
    def __str__(self):
        return self.nombre

class Curso(models.Model):
    titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField()
    estado = models.BooleanField(null=False,blank=False,default=False)
    centro = models.ForeignKey('Centro',on_delete=models.DO_NOTHING)   
    def __str__(self):
        return self.titulo

class Tarea(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,null=True,blank=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField(default=None, blank=True, null=True)
    enunciado = models.TextField()
    nota_maxima = models.FloatField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    min_exercise_version = models.FloatField(default=0, null=True, blank=True)
    ejercicio = models.ForeignKey('Ejercicio',on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.titulo

class Ejercicio(models.Model):
    titulo = models.CharField(max_length=100,null=False,blank=False)
    idVr = models.CharField(max_length=100,null=False,blank=False)
    def __str__(self):
        return self.titulo


class Entrega(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    fecha_edicion = models.DateTimeField(default=timezone.now)
    archivo = models.FileField(upload_to='static/assets/archivos',default=None, blank=True, null=True)
    auto_puntuacion = models.ForeignKey('Auto_Puntuacion',on_delete=models.DO_NOTHING,default=None,blank=True,null=True)
    comentario_alumno = models.CharField(max_length=500,default=None, blank=True, null=True)
    tarea = models.ForeignKey('Tarea',on_delete=models.DO_NOTHING,null=False) 
    nota = models.FloatField(null=True,blank=True,default=True)

    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)

    def __str__(self):
        return str(self.id)

class Calificacion(models.Model):
    tarea = models.ForeignKey('Tarea',on_delete=models.DO_NOTHING,null=False,default=False)
    alumno = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    nota = models.FloatField(null=True,blank=True,default=True)
    comentario = models.CharField(max_length=500,default=None, blank=True, null=True)
    fecha_calificacion = models.DateTimeField(default=None, blank=True, null=True)
    profesor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=None, blank=True, null=True, related_name='profesor')

    def __str__(self):
        return str(self.tarea) + "-" + str(self.alumno)

class Link(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING,default=True)
    titulo = models.CharField(max_length=100)
    link = models.URLField(null=False)
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

class Texto(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING,default=True)
    titulo = models.CharField(max_length=100)
    texto = models.TextField(null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

class Documento(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING,default=True)
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='documents/',null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

class Tipo_Subscripcion(models.Model):
    nombre = models.CharField(max_length=100,null=False,blank=False)
    def __str__(self):
        return self.nombre

class Usuario_Curso(models.Model):
    class Meta:
        unique_together = ('usuario', 'curso','tipo_subscripcion')
    usuario = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.CASCADE)
    tipo_subscripcion = models.ForeignKey('Tipo_Subscripcion',on_delete=models.CASCADE)

class Invitacion(models.Model):
    email = models.EmailField(max_length=100)
    curso = models.ForeignKey('Curso',on_delete=models.CASCADE)
    tipo_subscripcion = models.ForeignKey('Tipo_Subscripcion',on_delete=models.CASCADE)

class Pin(models.Model):
    pin = models.CharField(max_length=4,unique=True,null=False)
    tarea = models.ForeignKey('Tarea',on_delete=models.DO_NOTHING,null=False,default=False)
    usuario = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=40,null=True,blank=True)
    @property
    def vigente(self):
        # admitimos PINs dentro de las 24h de su creación
        if self.fecha_creacion+datetime.timedelta(hours=24) > timezone.now():
            return True
        return False
    def genera(self):
        # genera nuevo PIN y mantiene el objeto y relaciones
        randomnum = random.randint(1000,9999)
        cuenta = 0
        while True:
            # protegemos contra bucle infinito
            cuenta += 1
            if cuenta>1000:
                randomnum = 0
                break
            # iteramos hasta que encontremos un numero PIN libre
            if not Pin.objects.filter(pin=randomnum).exists():
                break
            randomnum = random.randint(1000,9999)
        self.pin = randomnum
        return randomnum

class Auto_Puntuacion(models.Model):
    passed_items = models.IntegerField(null=False,blank=False,default=0)
    failed_items = models.IntegerField(null=False,blank=False,default=0)
    score = models.IntegerField(null=False,blank=False,default=0)
    comments = models.CharField(max_length=500,default=None, blank=True, null=True)

