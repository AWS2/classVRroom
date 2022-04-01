from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from .models import *


def index(request):
    return render(request, 'vroom/index.html')

@login_required
def entrega(request):
    print(request.POST)
    if(request.POST.get('id')):
        print('post recogido')
        contexto = {
            "id": request.POST.get('id'),
        }
        return render(request, 'vroom/entrega.html', contexto)
    print('NO post recogido')
    return render(request, 'vroom/entrega.html')

@login_required
def dashboard(request):
    return render(request, 'vroom/dashboard.html')

@login_required
def curso(request):
    if (request.POST.get('curso')): 
        id_curso = request.POST.get('curso')

        curso = Curso.objects.get(id = id_curso)

        tareas = list(Tarea.objects.filter(curso = id_curso).values())
        for tarea in tareas:
            tarea["tipo"] = "tarea"
        links = list(Link.objects.filter(curso = id_curso).values())
        for link in links:
            link["tipo"] = "link"
        textos = list(Texto.objects.filter(curso = id_curso).values())
        for texto in textos:
            texto["tipo"] = "texto"
        documentos = list(Documento.objects.filter(curso = id_curso).values())
        for documento in documentos:
            documento["tipo"] = "documento"
        
        contenidos = tareas+links+textos+documentos   
        contenidos = sorted(contenidos, key=lambda contenido: contenido.get("fecha_publicacion"))

        rol = Usuario_Curso.objects.get(usuario = request.user.id, curso = id_curso).tipo_subscripcion.nombre

        contexto = {
            "curso": curso,
            "contenidos": contenidos,
            "rol": rol
        }

        return render(request, 'vroom/curso.html', contexto)

from django.forms.models import model_to_dict

@login_required
def tarea(request):
    if (request.POST.get('id')):
        tarea = Tarea.objects.get(id = request.POST.get('id'))

        tarea_dict = model_to_dict(tarea)
        tarea_dict["curso_nombre"]= tarea.curso.titulo

        rol = Usuario_Curso.objects.get(usuario = request.user, curso = tarea.curso).tipo_subscripcion

        if (rol.nombre == "Alumno"):
            try:
                entrega = (Entrega.objects.filter(tarea = tarea.id, autor = request.user).values())
                entrega = list(entrega)[0]
                try:
                    profesor = Usuario.objects.get(id = entrega["profesor_id"])
                    entrega["profesor"] = profesor.first_name + " " + profesor.last_name
                except:
                    entrega["profesor"] = False
            except:
                entrega = False

            contexto = {
                "tarea": tarea_dict,
                "entrega": entrega
            }

            return render(request, 'vroom/tarea_alumno.html', contexto)

        else:
            
            alumnos_curso = list(Usuario_Curso.objects.filter(curso = tarea.curso, tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Alumno").id).values())

            alumnos = []
            for alumno in alumnos_curso:
                try:
                    ultima_entrega = (Entrega.objects.filter(tarea = tarea.id, autor = alumno["usuario_id"]).latest('fecha_edicion')).fecha_edicion
                except:
                    ultima_entrega = False
                id_alumno = alumno["usuario_id"]
                dict_alumno = model_to_dict(Usuario.objects.get(id = id_alumno))
                dict_alumno["ultima_entrega"] = ultima_entrega
                alumnos.append(dict_alumno)
                
            contexto = {
                "tarea": tarea_dict,
                "alumnos": list(alumnos)
            }

            return render(request, 'vroom/tarea_profesor.html', contexto)