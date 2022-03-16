"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('api/tipo_ejercicio/<int:id_tipo>', views.tipo_ejercicio, name='tipo_ejercicio')
]