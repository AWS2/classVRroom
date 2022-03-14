from django.http import JsonResponse
from vroom.models import *

def ping(request):
    if (request.method=='GET'):
        return JsonResponse({
            'ping': 'pong'
        })

def cursos(request):
    centro = request.GET['id_centro']
    cursos = Curso.objects.filter()
    return JsonResponse({
        'centro': centro
    })