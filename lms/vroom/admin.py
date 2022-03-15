from django.contrib import admin

from .models import *

from django.contrib import admin
from .models import *
 
# Register your models here.
 
class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    fields = ('autor','titulo','enunciado','nota_maxima','tipo_ejercicio')  
    readonly_fields = ('autor','titulo')
    extra = 0
 
class EntregaInline(admin.TabularInline):
    model = Entrega
    fields = ('autor','fecha_publicacion','ejercicio')
    readonly_fields = ('autor',)
    extra = 0
 
class LinkInline(admin.TabularInline):
    model = Link
    fields = ('autor','titulo','link')
    extra = 0
 
class TextoInline(admin.TabularInline):
    model = Texto
    fields = ('autor','titulo','texto')
    extra = 0
 
class DocumentoInline(admin.TabularInline):
    model = Documento
    readonly_fields = ('autor',)
    fields = ('autor','titulo','archivo')
    extra = 0
 
 
 
class Usuario_CursoInline(admin.TabularInline):
    model = Usuario_Curso
    verbose_name = "Suscripcion"
    verbose_plural_name = "Suscripciones"
    fields = ('usuario','tipo_subscripcion',)
    readonly_fields = ('usuario','tipo_subscripcion')
    extra = 0
 
 
class EjercicioAdmin(admin.ModelAdmin):
    list_display= ('titulo','get_Curso',)
 
    def get_Curso(self,obj):
        return obj.curso.titulo
    get_Curso.short_description = 'Curso'
 
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        cursos = Curso.objects.filter(centro = request.user)
        return qs.filter(curso__in=cursos)
    inlines = [EntregaInline]
 
class EntregaAdmin(admin.ModelAdmin):
    list_display= ('id','get_Ejercicio','get_Autor')
   
    def get_Ejercicio(self,obj):
        return obj.ejercicio.titulo
    get_Ejercicio.short_description = 'Ejercicio'
 
    def get_Autor(self,obj):
        print(obj.autor.username)
        return str(obj.autor.get_full_name())
    get_Autor.short_description = 'Autor'
 
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        cursos = Curso.objects.filter(centro = request.user)
        ejercicios = Ejercicio.objects.filter(curso__in = cursos)
        return qs.filter(ejercicio__in = ejercicios)
 
class CursoAdmin(admin.ModelAdmin):
   
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(centro=request.user)
    inlines = [LinkInline, TextoInline ,DocumentoInline, EjercicioInline, Usuario_CursoInline ]

admin.site.register(Centro)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Ejercicio, EjercicioAdmin)
admin.site.register(Tipo_Ejercicio)
