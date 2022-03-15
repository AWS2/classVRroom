from django.urls import path

from . import views

urlpatterns = [
    path('', views.entrega, name='entrega'),
]