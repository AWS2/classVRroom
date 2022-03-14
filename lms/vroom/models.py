from django.db import models
from django.contrib.auth.models import AbstractUser



class Usuario(AbstractUser):
    terminos = models.ForeignKey('Terminos',on_delete=models.DO_NOTHING,null=True) 

    def __str__(self):
        return self.username

Usuario._meta.get_field('email')._unique = True

class Terminos(models.Model):
    version = models.FloatField()
    permisos = models.IntegerField()
    texto = models.TextField(null=True)

class Centro(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.ImageField()
    administrador = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)

class Curso(models.Model):
    titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField()
    estado = models.BooleanField(null=False,blank=False,default=False)
    centro = models.ForeignKey('Centro',on_delete=models.DO_NOTHING,default=True)

    def __str__(self):
        return self.titulo

class Ejercicio(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING,default=True)
    titulo = models.CharField(max_length=100,null=False,blank=False)
    descripcion = models.TextField()
    enunciado = models.TextField()
    nota_maxima = models.FloatField()
    tipo_ejercicio = models.ForeignKey('Tipo_Ejercicio',on_delete=models.DO_NOTHING,default=True)

    def __str__(self):
        return self.titulo

class Entrega(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    fecha_publicacion = models.DateTimeField()
    fecha_edicion = models.DateTimeField()
    archivo = models.FileField(upload_to='monka/',null=True)
    comentario_alumno = models.CharField(max_length=500)
    comentario_profesor = models.CharField(max_length=500)
    ejercicio = models.ForeignKey('Ejercicio',on_delete=models.DO_NOTHING,null=False) 
    nota = models.FloatField(null=True,blank=True,default=True)

    def __str__(self):
        return str(self.id)

class Link(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING,default=True)
    titulo = models.CharField(max_length=100)
    link = models.URLField(null=False)

    def __str__(self):
        return self.titulo

class Texto(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING,default=True)
    titulo = models.CharField(max_length=100)
    texto = models.TextField(null=True)

    def __str__(self):
        return self.titulo

class Documento(models.Model):
    autor = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.DO_NOTHING,default=True)
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='documents/',null=True)

    def __str__(self):
        return self.titulo

class Tipo_Ejercicio(models.Model):
    nombre = models.CharField(max_length=30)
    icono = models.ImageField()

    def __str__(self):
        return self.nombre

class Tipo_Subscripcion(models.Model):
    nombre = models.CharField(max_length=100,null=False,blank=False)

class Usuario_Curso(models.Model):
    usuario = models.ForeignKey('Usuario',on_delete=models.DO_NOTHING,default=True)
    curso = models.ForeignKey('Curso',on_delete=models.CASCADE)
    tipo_subscripcion = models.ForeignKey('Tipo_Subscripcion',on_delete=models.CASCADE)

class Invitacion(models.Model):
    email = models.EmailField(max_length=100)
    curso = models.ForeignKey('Curso',on_delete=models.CASCADE)
    tipo_subscripcion = models.ForeignKey('Tipo_Subscripcion',on_delete=models.CASCADE)