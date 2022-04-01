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
        serializer = self.serializer_class(data=request.data,
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
            'token': token.key,
            'status': 'OK',
            'message': 'Exercise data successfully stored.'
        })


#API
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    path('api/ping', views.ping, name='ping'),
    path('api/usuario/<int:id_usuario>', views.usuario, name='usuario'),
    path('api/cursos/<int:id_centro>', views.cursos, name='cursos'),
    path('api/curso/<int:id_curso>', views.curso, name='curso'),
    path('api/tareas/<int:id_curso>', views.tareas, name='tareas'),
    path('api/tarea/<int:id_tarea>', views.tarea, name='tarea'),
    path('api/entregas/<int:id_tarea>', views.entregas, name='entregas'),
    path('api/entrega/<int:id_entrega>', views.entrega, name='entrega'),
    path('api/calificaciones/<int:id_tarea>', views.calificaciones, name='calificaciones'),
    path('api/entrega_alumno/<int:tarea_id>/', views.entrega_alumno, name='entrega alumno'),
    path('api/usuario_cursos/<int:id_usuario>', views.usuario_cursos, name='usuario_cursos'),
    path('api/login_usuario', apiviews.obtain_auth_token, name='login_usuario'),
    path('api/login',CustomAuthToken.as_view(),name="login_api"),
    path('api/logout', views.logout_usuario,  name='logout_usuario'),
    path('api/get_courses', views.get_courses, name='get_courses'),
    path('api/get_course_details', views.get_course_details, name='get_courses_details'),
    path('api/pin_request',views.pin_request, name="pin_request"),
    path('api/start_vr_exercise',views.start_vr_exercise, name="start_vr_exercise"),
    path('api/finish_vr_exercise',views.finish_vr_exercise, name="finish_vr_exercise"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
