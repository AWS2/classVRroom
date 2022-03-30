from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vroom.urls')),
]



#API
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    path('api/ping', views.ping, name='ping'),
    path('api/usuario/<int:id_usuario>', views.usuario, name='usuario'),
    path('api/cursos/<int:id_centro>', views.cursos, name='cursos'),
    path('api/curso/<int:id_curso>', views.curso, name='curso'),
    path('api/ejercicios/<int:id_curso>', views.ejercicios, name='ejercicios'),
    path('api/ejercicio/<int:id_ejercicio>', views.ejercicio, name='ejercicio'),
    path('api/entregas/<int:id_ejercicio>', views.entregas, name='entregas'),
    path('api/entrega/<int:id_entrega>', views.entrega, name='entrega'),
    path('api/entrega_nueva_cal/<int:ejercicio_id>/', views.entrega_nueva_cal, name='nueva calificacion'),
    path('api/entrega_alumno/<int:ejercicio_id>/', views.entrega_alumno, name='entrega alumno'),
    path('api/tipo_ejercicio/<int:id_tipo>', views.tipo_ejercicio, name='tipo_ejercicio'),
    path('api/usuario_cursos/<int:id_usuario>', views.usuario_cursos, name='usuario_cursos')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
