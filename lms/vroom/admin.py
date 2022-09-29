from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.db import IntegrityError, transaction
from .models import *
 
# Register your models here.

class TerminoAdmin(admin.ModelAdmin):
    model = Termino
    list_display = ('version','permisos','texto')
  
class TareaInline(admin.TabularInline):
    model = Tarea
    fields = ('titulo','enunciado','nota_maxima', 'fecha_publicacion', 'ejercicio')  
    extra = 0
    def save_model(self,request,obj,form,change):
        print("saving...")
        return super().save_model(request,obj,form,change)

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
    def formfield_for_foreignkey(self,db_field,request=None,**kwargs):
        if db_field.name=="usuario" and not request.user.is_superuser:
            # restringir a alumnos del centro
            kwargs["queryset"] = Usuario.objects.filter(centro=request.user.centro)
        return super().formfield_for_foreignkey(db_field,request=request,**kwargs)
 
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
    edit_inlines = [LinkInline, TextoInline ,DocumentoInline, TareaInline, Usuario_CursoInline ]

    def get_form(self,request,obj=None,**kwargs):
        # por defecto cargamos los inlines
        self.inlines = self.edit_inlines
        if request.user.is_superuser:
            self.readonly_fields = ()
        else:
            self.readonly_fields = ('centro',)
            # cuando creamos nuevo curso, no ponemos inlines
            if obj==None:
                self.inlines = []
        return super().get_form(request,obj,**kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.es_admin:
            return qs.filter(centro=request.user.centro)
        elif request.user.es_profesor:
            subscripciones = request.user.usuario_curso_set.all()
            mis_cursos = subscripciones.values("curso")
            return qs.filter(id__in=mis_cursos)
        # aquí no se tendria que llegar
        return qs.objects.none()

    def save_model(self,request,obj,form,change):
        nuevo_curso = True
        if obj.pk: nuevo_curso = False
        # si es superuser lo dejamos como diga
        if request.user.is_superuser:
            super().save_model(request,obj,form,change)
            return
        if request.user.es_admin:
            # asociamos el nuevo usuario al centro del actual usuario
            obj.centro = request.user.centro
            super().save_model(request,obj,form,change)
            return
        if request.user.es_profesor:
            # asociamos el nuevo usuario al centro del actual usuario
            obj.centro = request.user.centro
            super().save_model(request,obj,form,change)
            # intentamos inscribir al profesor en el curso al crear curso
            if nuevo_curso:
                subsProfe = Tipo_Subscripcion.objects.get(nombre='Profesor')
                subscripcion = Usuario_Curso(usuario=request.user,
                            curso=obj,tipo_subscripcion=subsProfe)
                # no necesita protección porque en creación se desactivan los inlines
                subscripcion.save()
            return
        # si no es admin_centro ni superuser no se guarda nada
        # Dar error (ningun usuario debería llegar aquí)
        print("ERROR: en UserAdmin.save_model (usuario no autorizado)")
        raise Exception("Usuario no autorizado. Hablar con el administrdor.")


from django.contrib.auth.forms import UserCreationForm
class UserCreateForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'first_name' , 'last_name', )

class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}
    list_display = UserAdmin.list_display + ('is_active','centro','get_permisos',)
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

    def get_form(self,request,obj=None,**kwargs):
        if request.user.is_superuser:
            self.readonly_fields = ()
        else:
            self.readonly_fields = ('centro','is_staff',
                    'is_superuser','groups','user_permissions')
        return super().get_form(request,obj,**kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.es_admin or request.user.es_profesor:
            return qs.filter(centro=request.user.centro)
        """elif request.user.es_profesor:
            # mostramos alumnos que el profesor tenga en algun curso
            # TODO: optimizar
            subs_profe = Tipo_Subscripcion.objects.get(nombre='Profesor')
            subscripciones = request.user.usuario_curso_set.filter(tipo_subscripcion=subs_profe)
            mis_cursos = Curso.objects.filter(id__in=subscripciones.values("curso"))
            alumno_ids = []
            for curso in mis_cursos:
                alumnos = curso.usuario_curso_set.filter(curso=curso).values("usuario")
                for alumno in alumnos:
                    #print(alumno)
                    alumno_ids.append(alumno["usuario"])
            #print(alumno_ids)
            return qs.filter(id__in=alumno_ids)"""
        # no se tendria que llegar aqui
        print("none!")
        return Usuario.objects.none()

    def save_model(self,request,obj,form,change):
        # si es superuser lo dejamos como diga
        if request.user.is_superuser:
            super().save_model(request,obj,form,change)
            return
        # asociamos el nuevo usuario al centro del actual usuario
        if request.user.es_admin or request.user.es_profesor:
            obj.centro = request.user.centro
            obj.is_staff = False
            obj.is_superuser = False
            obj.save()
            return
        # si no es admin_centro ni superuser no se guarda nada
        # Dar error (ningun usuario debería llegar aquí)
        print("ERROR: en UserAdmin.save_model (usuario no autorizado)")
        raise Exception("Usuari no autorizado. Hablar con el administrdor.")


class PinAdmin(admin.ModelAdmin):
    model = Pin
    list_display = ('pin','vigente','usuario','tarea','get_curso','get_centro','fecha_creacion')
    search_fields = ('usuario__first_name','usuario__last_name',
            'usuario__email','tarea__titulo','tarea__curso__titulo')
    def get_curso(self,obj):
        return obj.tarea.curso.titulo
    def get_centro(self,obj):
        return obj.tarea.curso.centro.nombre
    def vigente(self,obj):
        return obj.vigente
    vigente.boolean = True

admin.site.register(Centro,CentroAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Tipo_Subscripcion)
admin.site.register(Usuario, UserAdmin)
admin.site.register(Termino,TerminoAdmin)
#admin.site.register(Entrega)
#admin.site.register(Usuario_Curso)
admin.site.register(Pin,PinAdmin)
#admin.site.register(Calificacion)
#admin.site.register(Auto_Puntuacion)
admin.site.register(Ejercicio)
