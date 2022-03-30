from enum import auto
from webbrowser import get
from django.http import JsonResponse
from django.http import Http404
from vroom.models import *
from django.contrib.auth.models import User, Group
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import random
import json

def ping(request):
    if (request.method=='GET'):
        return JsonResponse({
            'ping': 'pong'
        })



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def start_vr_exercise(request):
    getpin=request.GET.get('pin')
    
    
    try:
        pin = Pin.objects.get(pin=getpin)
    except:
        
        return Response({
            'status': 'ERROR',
            'message': 'Pin no encontrado.'
        })
    

    user = pin.usuario
    vr_exerciseid = pin.ejercicio.pk
    minVer = Ejercicio.objects.get(pk=vr_exerciseid).min_exercise_version
    if (minVer == None):
        minVer = None
    return Response({
        "status" : "OK",
        "username": user.first_name+" "+user.last_name,
        "VRexerciseID" :  vr_exerciseid,
        "minExerciseVersion" : minVer,
    })



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def finish_vr_exercise(request):
    getpin=request.GET.get('pin')
    autograde=request.GET.get('autograde')
    VRexerciseID=request.GET.get('VRexerciseID')
    exerciseVersionID=request.GET.get('exerciseVersionID')

    if getpin==None or autograde==None or VRexerciseID==None or exerciseVersionID==None:
        return Response({
            'status': 'ERROR',
            'message': 'Faltan parametros.'
        })

    try:
        pin = Pin.objects.get(pin=getpin)
    except:
        
        return Response({
            'status': 'ERROR',
            'message': 'Pin no encontrado.'
        })

    try:
        ejercicio = Ejercicio.objects.get(pk=VRexerciseID, min_exercise_version=exerciseVersionID)
    except:
  
        return Response({
            'status': 'ERROR',
            'message': 'Ejercicio no encontrado.'
        })
    
    try:
        entrega = Entrega.objects.get(autor=request.user,ejercicio=ejercicio)

    except:

        entrega = Entrega.objects.create(
            autor=request.user,
            fecha_publicacion=timezone.now(),
            fecha_edicion=timezone.now(),
            ejercicio=ejercicio,
        )



    

    autograde = json.loads(autograde)

    print(autograde)

    ejercicio.nota_maxima=autograde['total_items']

    ejercicio.save()

    entrega.nota=autograde['passed_items']
    
    entrega.save()

    pin.delete()

    return Response({
        'status': 'OK',
        'message': 'Exercise data successfully stored.'
    })



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pin_request(request):

    VRtaskID = request.GET.get('VRtaskID')

    print(VRtaskID)

    try:
        ejercicio = Ejercicio.objects.get(id=VRtaskID)
    except:
        return Response({
            "status" : "ERROR",
            "message" : "Ejercicio no encontrado",
        })

    while True:
        randomnum = random.randint(1000,9999)

        try:
            if(Pin.objects.filter(ejercicio=ejercicio, usuario=request.user).exists()):
                return Response({
                    "status" : "ERROR",
                    "message" : "Ya existe un pin para este usuario",
                })
            Pin.objects.get(pin=randomnum)

        except:
            break




    new_pin = Pin.objects.create(
        pin = randomnum,
        ejercicio = ejercicio,
        usuario = request.user
    )

    new_pin.save()

    return Response({
        'status':'OK',
        'message': 'VRtaskID is required',
        'PIN': new_pin.pin
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_course_details(request):

    id_curso=request.GET.get('courseID')
    subscripcion_profesor = Tipo_Subscripcion.objects.get(nombre = "Profesor")
    curso = Curso.objects.get( pk = id_curso)
    content = {"title": curso.titulo,"description": curso.descripcion,"courseID": curso.pk,"institutionID": curso.centro.pk,"status": curso.estado,'elements':{'links':[],'texts':[],'documents':[],'tasks':[]} }
    if(id_curso == None):
        return Response({
        "status" : 'ERROR',
        "message" : 'courseID is required'
    })
        


    links = Link.objects.filter(pk = id_curso)
    links_items = []
    for link in links:
        links_items.append({"linkID": link.pk, "title": link.titulo, "link": link.link})   
    content['elements']['links'] = links_items
    
    textos = Texto.objects.filter(pk = id_curso)
    textos_items = []
    for texto in textos:
        textos_items.append({"textID": texto.pk, "autorID":texto.autor.id, "title": texto.titulo, "texto": texto.texto})
    content['elements']['texts'] = textos_items
    
    documents = Documento.objects.filter(pk = id_curso)
    documents_items = []
    for document in documents:
        documents_items.append({"documentID": document.pk, "autorID":document.autor.id, "file":document.archivo.url})
    content['elements']['documents'] = documents_items
    
    tasks = Ejercicio.objects.filter(pk = id_curso)
    tasks_items = []
    for task in tasks:
        tasks_items.append({"taskID": task.pk, "title": task.titulo, "description": task.descripcion, "quote": task.enunciado, "maxQualification": task.nota_maxima, "task_type": task.tipo_ejercicio.nombre})
    content['elements']['tasks'] = tasks_items
          
               
    return Response({
        "status" : 'OK',
        "course_list": content
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_courses(request):

    cursos = Curso.objects.all()

    content = []
    subscripcion_profesor = Tipo_Subscripcion.objects.get(nombre = "Profesor")
    subscripcion_alumno = Tipo_Subscripcion.objects.get(nombre = "Alumno")

    for icurso in cursos:
        curso_item ={"courseID": icurso.pk, "title": icurso.titulo, "description": icurso.descripcion, "status": icurso.estado,"center": icurso.centro.pk,'subscribers':{'teachers':[],'students':[]}}      
        profesor_curso = Usuario_Curso.objects.get( curso = icurso, tipo_subscripcion = subscripcion_profesor)

        print(profesor_curso)
        if(not profesor_curso == None):    
            curso_item['subscribers']['teachers'].append({"UserID": profesor_curso.usuario.pk, "username": profesor_curso.usuario.username, "email":profesor_curso.usuario.email})
        alumnos_curso = Usuario_Curso.objects.filter( curso = icurso, tipo_subscripcion = subscripcion_alumno).all()
        alumno_item_list = []
        if(not alumnos_curso == None):
            for alumno in alumnos_curso:
                alumno_item_list.append({"UserID": alumno.usuario.pk,"username":alumno.usuario.username, "email":alumno.usuario.email})

            curso_item['subscribers']['students'] = alumno_item_list
        content.append(curso_item)
        
            
    return Response({
        "status" : 'OK',
        "course_list": content
        })
    
    ##except:
        #return Response({
         #   "status" : 'ERROR',
          #  "message": 'session_token is required'
           # })


#Api de deslogueo
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_usuario(request):

    request.user.auth_token.delete()
    
    content = {
        'status': 'OK',
        'message': 'Session successfully closed.',
    }
    return Response(content)

@login_required
def usuario(request, id_usuario):
    if (request.method=='GET'):

        #proteccion: ser su profe, su admin, el usuario o el super
        subscripcion_profesor = Tipo_Subscripcion.objects.filter(nombre = "Profesor")
        subscripcion_alumno = Tipo_Subscripcion.objects.filter(nombre = "Alumno")
        cursos_alumno = Usuario_Curso.objects.filter(usuario = id_usuario, tipo_subscripcion__in = subscripcion_alumno).values('curso')
        cursos_profe = Usuario_Curso.objects.filter(usuario = request.user.id, tipo_subscripcion__in = subscripcion_profesor).values('curso')
        cursos_admin = Curso.objects.filter(centro__in = Centro.objects.filter(administrador = request.user.id)).values('id')
        cursos_con_profesor = Usuario_Curso.objects.filter(curso__in = cursos_alumno).filter(curso__in = cursos_profe)
        cursos_con_admin = Usuario_Curso.objects.filter(curso__in = cursos_alumno).filter(curso__in = cursos_admin)

        if (len(cursos_con_profesor) == 0 and len(cursos_con_admin) == 0 and not request.user.id == id_usuario and not request.user.is_superuser):
            raise PermissionDenied()     
        #fin proteccion   

        usuario = Usuario.objects.filter(id = id_usuario).values()

        if (len(usuario) == 0):
            raise Http404()
        
        return JsonResponse({
            'data': list(usuario)
        })


@login_required
def cursos(request, id_centro):
    if (request.method=='GET'):
        cursos = Curso.objects.filter(centro = id_centro).values()

        if (len(cursos) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(cursos)
        })

@login_required
def curso(request, id_curso):
    if (request.method=='GET'):
        curso = Curso.objects.filter(id = id_curso).values()

        if (len(curso) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(curso) 
        })

@login_required
def ejercicios(request, id_curso):
    if (request.method=='GET'):

        #proteccion: estar subscrito al curso, ser el admin del centro, o ser el super
        subscripcion = Usuario_Curso.objects.filter(usuario = request.user.id, curso = id_curso)
        admin_curso = Curso.objects.filter(centro__in = Centro.objects.filter(administrador = request.user.id), id = id_curso)

        if (len(subscripcion) == 0 and len(admin_curso) == 0 and not request.user.is_superuser):
            raise PermissionDenied()     
        #fin proteccion   

        ejercicios = Ejercicio.objects.filter(curso = id_curso).values()

        if (len(ejercicios) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(ejercicios)
        })

@login_required
def ejercicio(request, id_ejercicio):
    if (request.method=='GET'):
        
        #proteccion: estar subscrito al curso, ser el admin del centro, o ser el super
        curso = Curso.objects.get(id = Ejercicio.objects.get(id = id_ejercicio).curso.id)
        subscripcion = Usuario_Curso.objects.filter(usuario = request.user.id, curso = curso.id)
        admin_curso = Curso.objects.filter(centro__in = Centro.objects.filter(administrador = request.user.id), id = curso.id)

        if (len(subscripcion) == 0 and len(admin_curso) == 0 and not request.user.is_superuser):
            raise PermissionDenied()     
        #fin proteccion
        
        ejercicio = Ejercicio.objects.filter(id = id_ejercicio).values()

        if (len(ejercicio) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(ejercicio) 
        })

@login_required
def entregas(request, id_ejercicio):
    if (request.method=='GET'):

        #proteccion: ser profesor del curso, ser el admin del centro o ser el super
        curso = Curso.objects.get(id = Ejercicio.objects.get(id = id_ejercicio).curso.id)
        profesor = Usuario_Curso.objects.filter(usuario = request.user.id, curso = curso.id, tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Profesor"))
        admin = Curso.objects.filter(centro__in = Centro.objects.filter(administrador = request.user.id), id = curso.id)

        if (len(profesor) == 0 and len(admin) == 0 and not request.user.is_superuser):
            raise PermissionDenied()
        #fin proteccion

        entregas = Entrega.objects.filter(ejercicio = id_ejercicio).values()

        if (len(entregas) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(entregas)
        })

@login_required
@csrf_exempt
def entrega(request, id_entrega):
    if (request.method=='GET'):
        

        #proteccion: ser profesor del curso, ser el admin del centro, ser el autor de la entrega o ser el super
        entrega = Entrega.objects.get(id = id_entrega)
        curso = Curso.objects.get(id = Ejercicio.objects.get(id = entrega.ejercicio.id).curso.id)
        profesor = Usuario_Curso.objects.filter(usuario = request.user.id, curso = curso.id, tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Profesor"))
        admin = Curso.objects.filter(centro__in = Centro.objects.filter(administrador = request.user.id), id = curso.id)

        if (len(profesor) == 0 and len(admin) == 0 and not entrega.autor == request.user.id and not request.user.is_superuser):
            raise PermissionDenied()
        #fin proteccion

        entrega = Entrega.objects.filter(id = id_entrega).values()

        if (len(entrega) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(entrega) 
        })

    elif (request.method=='PUT'): #para actualizar/poner la nota y/o el comentario del profesor
    
        #proteccion: ser profesor del curso, ser el admin del centro o ser el super
        entrega = Entrega.objects.get(id = id_entrega)
        curso = Curso.objects.get(id = Ejercicio.objects.get(id = entrega.ejercicio.id).curso.id)
        profesor = Usuario_Curso.objects.filter(usuario = request.user.id, curso = curso.id, tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Profesor"))
        admin = Curso.objects.filter(centro__in = Centro.objects.filter(administrador = request.user.id), id = curso.id)

        if (len(profesor) == 0 and len(admin) == 0 and not request.user.is_superuser):
            raise PermissionDenied()
        #fin proteccion

        entrega = Entrega.objects.filter(id = id_entrega).values()
        ejercicio = Ejercicio.objects.get(id__in = Entrega.objects.filter(id = id_entrega).values('ejercicio'))

        if (len(entrega) == 0 or ejercicio is None):
            raise Http404()

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        if 'new_note' in body and 'comment_prof' in body:
            max_note = ejercicio.nota_maxima
            note = float(body['new_note'])
            comment = str(body['comment_prof'])
  

            if not note==None and max_note:
                if note <0:
                    return JsonResponse({"msg": "La nota no puede ser negativa", "tipo": "danger"})
                elif note <= max_note:
                    entrega.update(profesor = request.user)
                    entrega.update(nota=note)
                    entrega.update(comentario_profesor=comment)
                    entrega.update(fecha_calificacion=timezone.now())
                    return JsonResponse({"msg": "Calificación actualizada", "tipo": "success"})  
                else :
                    return JsonResponse({"msg": "La nota no puede superar la nota máxima", "tipo": "danger"})
            else:
                return JsonResponse({"msg": "Faltan datos", "tipo": "danger"})

        return JsonResponse({
            'data': list(entrega) 
        })

@csrf_exempt
@login_required
def entrega_nueva_cal(request, ejercicio_id):
    if (request.method=='POST'):

        #proteccion: ser subscriptor del curso, ser el admin del centro o ser el super
        curso = Curso.objects.get(id = Ejercicio.objects.get(id = ejercicio_id).curso.id)
        profesor = Usuario_Curso.objects.filter(usuario = request.user.id, curso = curso.id, tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Profesor"))
        admin = Curso.objects.filter(centro__in = Centro.objects.filter(administrador = request.user.id), id = curso.id)

        if (len(profesor) == 0 and len(admin) == 0 and not request.user.is_superuser):
            raise PermissionDenied()
        #fin proteccion
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        nota = float(body['new_note'])
        nota_maxima = Ejercicio.objects.get(id = ejercicio_id).nota_maxima

        if nota>nota_maxima:
            return JsonResponse({"msg": "La nota no puede superar la nota máxima", "tipo": "danger"})
        elif nota>=0:
            comentario = str(body['comment_prof'])
            autor = str(body['autor'])
            entrega = Entrega.objects.create(ejercicio = Ejercicio.objects.get(id=ejercicio_id), autor_id = autor, profesor = request.user, nota = nota, comentario_profesor = comentario, fecha_calificacion = timezone.now())
            return JsonResponse({"msg": "Calificación creada", "tipo": "success"})
        else:
            return JsonResponse({"msg": "Faltan datos", "tipo": "danger"})

@csrf_exempt
def entrega_alumno(request, ejercicio_id):
    print(request.POST)
    if (request.method=='POST'):

        #proteccion: ser alumno en el curso del ejercicio o ser el super
        ejercicio = Ejercicio.objects.get(id = ejercicio_id)
        curso = ejercicio.curso
        try:
            alumno = Usuario_Curso.objects.get(usuario = request.user.id, curso = curso.id, tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Alumno"))
        except:
            raise PermissionDenied()
        #fin proteccion

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        comentario = str(body['comentario'])
        entrega = Entrega.objects.filter(ejercicio = ejercicio_id, autor_id = request.user.id).values()
        if (len(entrega) == 0):
            Entrega.objects.create(ejercicio = ejercicio, autor = request.user, comentario_alumno = comentario, fecha_publicacion = timezone.now(), fecha_edicion = timezone.now(), nota = None)
            return JsonResponse({"msg": "Entrega creada", "tipo": "success"})
        
        else:
            entrega.update(comentario_alumno = comentario)
            entrega.update(fecha_edicion = timezone.now())
            return JsonResponse({"msg": "Entrega actualizada", "tipo": "success"})

        return JsonResponse({"msg": "Algo ha ido mal", "tipo": "danger"})

    


@login_required
def tipo_ejercicio(request, id_tipo):
    if (request.method=='GET'):
        tipo = Tipo_Ejercicio.objects.filter(id = id_tipo).values()

        if (len(tipo) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(tipo) 
        })

@login_required
def usuario_cursos(request, id_usuario):
    if (request.method=='GET'):

        #proteccion: es el usuario, es el super
        if (not request.user.id == id_usuario and not request.user.is_superuser):
            raise PermissionDenied()
        #fin proteccion

        cursos_id =  list(Usuario_Curso.objects.filter(usuario = id_usuario).values_list('curso', flat=True))
        cursos = Curso.objects.filter(id__in = cursos_id).values()

        for curso in cursos:
            if (not len(Usuario_Curso.objects.filter(usuario = id_usuario, curso = curso["id"], tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Profesor"))) == 0):
                curso["rol"] =  "Profesor"
            else:
                curso["rol"] = "Alumno"

            print(len(Usuario_Curso.objects.filter(usuario = id_usuario, curso = curso["id"], tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Profesor"))))

            

        if (len(cursos) == 0):
            raise Http404()

        return JsonResponse({
            'data': list(cursos)
        })


