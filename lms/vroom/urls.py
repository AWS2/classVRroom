from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('tablero/', views.dashboard, name='tablero'),
    path('entrega/', views.entrega, name='entrega'),
]


#autentificacion
from django.contrib.auth.views import LoginView,LogoutView
from .forms import CustomLoginForm

urlpatterns += [
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]