from django.http import JsonResponse
from django.http import Http404
from vroom.models import *
import json
from django.views.decorators.csrf import csrf_exempt

def ping(request):
    if (request.method=='GET'):
        return JsonResponse({
            'ping': 'pong'
        })

def usuario(request, id_usuario):
    if (request.method=='GET'):
        usuario = Usuario.objects.filter(id = id_usuario).values()

        if (len(usuario) == 0):
            raise Http404()
        
        return JsonResponse({
            'data': list(usuario)
        })

def cursos(request, id_centro):
    if (request.method=='GET'):
        cursos = Curso.objects.filter(centro = id_centro).values()

        if (len(cursos) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(cursos)
        })
def curso(request, id_curso):
    if (request.method=='GET'):
        curso = Curso.objects.filter(id = id_curso).values()

        if (len(curso) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(curso) 
        })

def ejercicios(request, id_curso):
    if (request.method=='GET'):
        ejercicios = Ejercicio.objects.filter(curso = id_curso).values()

        if (len(ejercicios) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(ejercicios)
        })
def ejercicio(request, id_ejercicio):
    if (request.method=='GET'):
        ejercicio = Ejercicio.objects.filter(id = id_ejercicio).values()

        if (len(ejercicio) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(ejercicio) 
        })

def entregas(request, id_ejercicio):
    if (request.method=='GET'):
        entregas = Entrega.objects.filter(ejercicio = id_ejercicio).values()

        if (len(entregas) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(entregas)
        })

@csrf_exempt
def entrega(request, id_entrega):
    if (request.method=='GET'):
        entrega = Entrega.objects.filter(id = id_entrega).values()


        if (len(entrega) == 0):
            raise Http404()



        return JsonResponse({
            'data': list(entrega) 
        })

    elif (request.method=='PUT'):

    
        entrega = Entrega.objects.filter(id = id_entrega).values()


        if (len(entrega) == 0):
            raise Http404()

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        if 'max_note' in body and 'new_note' in body and 'comment_prof' in body:
            max_note = float(body['max_note'])
            note = float(body['new_note'])
            comment = str(body['comment_prof'])
  

            if note and max_note:
                if note <= max_note:
                    entrega.update(nota=note)
                    entrega.update(comentario_profesor=comment)  
        

        return JsonResponse({
            'data': list(entrega) 
        })
        
def tipo_ejercicio(request, id_tipo):
    if (request.method=='GET'):
        tipo = Tipo_Ejercicio.objects.filter(id = id_tipo).values()


        if (len(tipo) == 0):
            raise Http404()



        return JsonResponse({
            'data': list(tipo) 
        })