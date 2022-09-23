from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
 
# Register your models here.

class TerminoAdmin(admin.ModelAdmin):
    model = Termino
    list_display = ('version','permisos','texto')
  
class TareaInline(admin.TabularInline):
    model = Tarea
    fields = ('titulo','enunciado','nota_maxima', 'fecha_publicacion', 'ejercicio')  
    extra = 0
 
class EntregaInline(admin.TabularInline):
    model = Entrega
    fields = ('autor','archivo','comentario_alumno', 'fecha_edicion')
    extra = 0
 
class CalificacionInline(admin.TabularInline):
    model = Calificacion
    fields = ('nota', 'comentario', 'fecha_calificacion', 'profesor')	
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    fields = ('titulo','link', 'fecha_publicacion')
    extra = 0
 
class TextoInline(admin.TabularInline):
    model = Texto
    fields = ('titulo','texto', 'fecha_publicacion')
    extra = 0
 
class DocumentoInline(admin.TabularInline):
    model = Documento
    fields = ('titulo','archivo', 'fecha_publicacion')
    extra = 0
 
class Usuario_CursoInline(admin.TabularInline):
    model = Usuario_Curso
    verbose_name = "Suscripcion"
    verbose_plural_name = "Suscripciones"
    fields = ('usuario','tipo_subscripcion',)
    extra = 0
 

class CentroAdmin(admin.ModelAdmin):
    list_display = ('nombre','administrador')


class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo','get_Curso',)
    readonly_fields = ('autor',)
    inlines = [EntregaInline, CalificacionInline]

    def get_Curso(self,obj):
        return obj.curso.titulo
    get_Curso.short_description = 'Curso'
 
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
    list_display = ('titulo','centro',)
    inlines = [LinkInline, TextoInline ,DocumentoInline, TareaInline, Usuario_CursoInline ]   
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.es_profesor:
            return qs.filter(centro=request.user.centro)
        # aquí no se tendria que llegar
        return qs.objects.none()


from django.contrib.auth.forms import UserCreationForm
class UserCreateForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'first_name' , 'last_name', )

class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}
    list_display = UserAdmin.list_display + ('centro','get_permisos',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'termino', 'date_joined', 'is_staff', 'is_active'),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
            ("Dades acadèmiques", {
                'fields': ('centro',),
            }),
    )
    def get_permisos(self, obj):
        permisos = ""
        for permiso in obj.groups.all():
            permisos += permiso.name + " "
        return permisos

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.es_admin:
            return qs.filter(centro=request.user.centro)
        elif request.user.es_profesor:
            return qs.filter(centro=request.user.centro)
        """    subProf = Tipo_Subscripcion.objects.get(nombre='Profesor')
            return qs.filter(id__in=(Usuario_Curso.objects.filter(usuario=request.user,tipo_subscripcion=subProf.id)).values('curso'))
        elif request.user.es_admin and \
            Centro.objects.filter(administrador=request.user).exists():
            return qs.filter(centro=Centro.objects.get(administrador=request.user))"""
        # no se tendria que llegar aqui
        print("none!")
        return Usuario.objects.none()


admin.site.register(Centro,CentroAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Tipo_Subscripcion)
admin.site.register(Usuario, UserAdmin)
admin.site.register(Termino,TerminoAdmin)
#admin.site.register(Entrega)
#admin.site.register(Usuario_Curso)
#admin.site.register(Pin)
#admin.site.register(Calificacion)
#admin.site.register(Auto_Puntuacion)
admin.site.register(Ejercicio)
