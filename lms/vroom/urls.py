from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('tablero/', views.dashboard, name='tablero'),
    path('curso/<int:id_curso>', views.curso, name='curso'),
    path('curso/<int:id_curso>/tarea/<int:id_tarea>', views.tarea, name='tarea'),
    path('curso/<int:id_curso>/tarea/<int:id_tarea>/entrega/<int:id_alumno>', views.entrega, name='entrega'),
    path('get_pin/<int:id_tarea>', views.get_pin, name="get_pin"),
]


#autentificacion
from django.contrib.auth.views import LoginView,LogoutView
from .forms import CustomLoginForm

urlpatterns += [
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

