import re
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views as apiviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vroom.urls')),
]


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def get(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.GET,
                                           context={'request': request})
        serializer.is_valid(raise_exception=False)



        try:
            user = serializer.validated_data['user']
        except:
            return Response({
                'status': 'ERROR',
                'message': 'Authentication error.'
            })

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'status': 'OK',
            'message': 'Autenticado con éxito.',
            'token': token.key,
        })


#API
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    path('api/ping', views.ping, name='api ping'),
    path('api/usuario/<int:id_usuario>', views.usuario, name='api usuario'),
    path('api/cursos/<int:id_centro>', views.cursos, name='api cursos'),
    path('api/curso/<int:id_curso>', views.curso, name='api curso'),
    path('api/tareas/<int:id_curso>', views.tareas, name='api tareas'),
    path('api/tarea/<int:id_tarea>', views.tarea, name='api tarea'),
    path('api/entregas/<int:id_tarea>', views.entregas, name='api entregas'),
    path('api/entrega/<int:id_entrega>', views.entrega, name='api entrega'),
    path('api/calificaciones/<int:id_tarea>', views.calificaciones, name='api calificaciones'),
    path('api/calificacion/<int:id_tarea>', views.calificacion, name='api calificacion'),
    path('api/entrega_alumno/<int:tarea_id>/', views.entrega_alumno, name='api entrega alumno'),
    path('api/usuario_cursos/<int:id_usuario>', views.usuario_cursos, name='api usuario_cursos'),
    path('api/login_usuario', apiviews.obtain_auth_token, name='api login_usuario'),
    path('api/login',CustomAuthToken.as_view(),name="api login_api"),
    path('api/logout', views.logout_usuario,  name='api logout_usuario'),
    path('api/get_courses', views.get_courses, name='api get_courses'),
    path('api/get_course_details', views.get_course_details, name='api get_courses_details'),
    path('api/pin_request',views.pin_request, name="api pin_request"),
    path('api/start_vr_exercise',views.start_vr_exercise, name="api start_vr_exercise"),
    path('api/finish_vr_exercise',views.finish_vr_exercise, name="api finish_vr_exercise"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
