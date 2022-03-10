from django.contrib import admin
from .models import * 

# Register your models here.

class LinkInline(admin.TabularInline):
    model = Link

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

admin.site.register(Curso)
admin.site.register(Ejercicio,EjercicioAdmin)
admin.site.register(Entrega,EntregaAdmin)
admin.site.register(Tipo_Ejercicio)
admin.site.register(Link)
admin.site.register(Documento)
admin.site.register(Text)