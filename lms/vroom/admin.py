from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
 
# Register your models here.
 
class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    fields = ('id', 'autor','titulo','enunciado','nota_maxima','tipo_ejercicio')  
    extra = 0
 
class EntregaInline(admin.TabularInline):
    model = Entrega
    fields = ('autor','fecha_publicacion','ejercicio')
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
    fields = ('autor','titulo','archivo')
    extra = 0
 
class Usuario_CursoInline(admin.TabularInline):
    model = Usuario_Curso
    verbose_name = "Suscripcion"
    verbose_plural_name = "Suscripciones"
    fields = ('usuario','tipo_subscripcion',)
    extra = 0
 
 
class EjercicioAdmin(admin.ModelAdmin):
    list_display= ('titulo','get_Curso',)
 
    def get_Curso(self,obj):
        return obj.curso.titulo
    get_Curso.short_description = 'Curso'
 
class EntregaAdmin(admin.ModelAdmin):
    list_display= ('id','get_Ejercicio','get_Autor')
   
    def get_Ejercicio(self,obj):
        return obj.ejercicio.titulo
    get_Ejercicio.short_description = 'Ejercicio'
 
    def get_Autor(self,obj):
        print(obj.autor.username)
        return str(obj.autor.get_full_name())
    get_Autor.short_description = 'Autor'
 
 
class CursoAdmin(admin.ModelAdmin):
   
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(centro=Centro.objects.get(administrador=request.user))
    inlines = [LinkInline, TextoInline ,DocumentoInline, EjercicioInline, Usuario_CursoInline ]

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
admin.site.register(Ejercicio, EjercicioAdmin)
admin.site.register(Tipo_Ejercicio)
admin.site.register(Usuario, UserAdmin)
admin.site.register(Termino)
admin.site.register(Entrega)