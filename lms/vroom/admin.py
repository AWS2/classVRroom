from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
 
# Register your models here.
 
class TareaInline(admin.TabularInline):
    model = Tarea
    fields = ('autor','titulo','enunciado','nota_maxima', 'fecha_publicacion')  
    extra = 0
 
class EntregaInline(admin.TabularInline):
    model = Entrega
    fields = ('autor', 'archivo','comentario_alumno', 'fecha_edicion')
    extra = 0
 
class CalificacionInline(admin.TabularInline):
    model = Calificacion
    fields = ('alumno', 'nota', 'comentario', 'fecha_calificacion', 'profesor')	
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    fields = ('autor','titulo','link', 'fecha_publicacion')
    extra = 0
 
class TextoInline(admin.TabularInline):
    model = Texto
    fields = ('autor','titulo','texto', 'fecha_publicacion')
    extra = 0
 
class DocumentoInline(admin.TabularInline):
    model = Documento
    fields = ('autor','titulo','archivo', 'fecha_publicacion')
    extra = 0
 
class Usuario_CursoInline(admin.TabularInline):
    model = Usuario_Curso
    verbose_name = "Suscripcion"
    verbose_plural_name = "Suscripciones"
    fields = ('usuario','tipo_subscripcion',)
    extra = 0
 
 
class TareaAdmin(admin.ModelAdmin):
    list_display= ('titulo','get_Curso',)
 
    def get_Curso(self,obj):
        return obj.curso.titulo
    get_Curso.short_description = 'Curso'
    inlines = [EntregaInline, CalificacionInline]
 
class EntregaAdmin(admin.ModelAdmin):
    list_display= ('id','get_Tarea','get_Autor')
   
    def get_Tarea(self,obj):
        return obj.tarea.titulo
    get_Tarea.short_description = 'Tarea'
 
    def get_Autor(self,obj):
        print(obj.autor.username)
        return str(obj.autor.get_full_name())
    get_Autor.short_description = 'Autor'
 
 
class CursoAdmin(admin.ModelAdmin):
   
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='profesor').exists(): 
            subProf = Tipo_Subscripcion.objects.get(nombre='Profesor')
            print(qs)
            return qs.filter(id__in = (Usuario_Curso.objects.filter(usuario=request.user,tipo_subscripcion=subProf.id)).values('curso'))
        else:
            return qs.filter(centro=Centro.objects.get(administrador=request.user))

    inlines = [LinkInline, TextoInline ,DocumentoInline, TareaInline, Usuario_CursoInline ]

from django.contrib.auth.forms import UserCreationForm
class UserCreateForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ('username', 'first_name' , 'last_name', )


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'termino', 'date_joined', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(Centro)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Tipo_Subscripcion)
admin.site.register(Usuario, UserAdmin)
admin.site.register(Termino)
admin.site.register(Entrega)
admin.site.register(Usuario_Curso)
admin.site.register(Pin)
admin.site.register(Calificacion)
admin.site.register(Auto_Puntuacion)