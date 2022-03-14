from django.urls import path

from . import views

app_name = 'vroom'
urlpatterns = [
    path('<int:id_ejercicio>', views.entrega, name='entrega'),
]