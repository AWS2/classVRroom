from django.urls import path

from . import views

urlpatterns = [
    path('', views.entrega, name='entrega'),
]





#autentificacion
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]