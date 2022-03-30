from django.http import JsonResponse
from django.http import Http404
from vroom.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone



def ping(request):
    if (request.method=='GET'):
        return JsonResponse({
            'ping': 'pong'
        })

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