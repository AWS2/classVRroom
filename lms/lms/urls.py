from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vroom.urls')),
]



#API
from . import views

urlpatterns += [
    path('api/ping', views.ping, name='ping'),
    path('api/usuario/<int:id_usuario>', views.usuario, name='usuario'),
    path('api/cursos/<int:id_centro>', views.cursos, name='cursos'),
    path('api/curso/<int:id_curso>', views.curso, name='curso'),
    path('api/ejercicios/<int:id_curso>', views.ejercicios, name='ejercicios'),
    path('api/ejercicio/<int:id_ejercicio>', views.ejercicio, name='ejercicio'),
    path('api/entregas/<int:id_ejercicio>', views.entregas, name='entregas'),
    path('api/entrega/<int:id_entrega>', views.entrega, name='entrega'),
    path('api/tipo_ejercicio/<int:id_tipo>', views.tipo_ejercicio, name='tipo_ejercicio'),
    path('api/usuario_cursos/<int:id_usuario>', views.usuario_cursos, name='usuario_cursos')
]