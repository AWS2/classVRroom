from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required


from .models import *


def index(request):
    return render(request, 'vroom/index.html')

@login_required
def entrega(request):
    return render(request, 'vroom/entrega.html')

@login_required
def dashboard(request):
    return render(request, 'vroom/dashboard.html')

@login_required
def curso(request):
    if (request.POST.get('curso')): 
        id_curso = request.POST.get('curso')

        curso = Curso.objects.get(id = id_curso)

        ejercicios = list(Ejercicio.objects.filter(curso = id_curso).values())
        for ejercicio in ejercicios:
            ejercicio["tipo"] = "ejercicio"
        links = list(Link.objects.filter(curso = id_curso).values())
        for link in links:
            link["tipo"] = "link"
        textos = list(Texto.objects.filter(curso = id_curso).values())
        for texto in textos:
            texto["tipo"] = "texto"
        documentos = list(Documento.objects.filter(curso = id_curso).values())
        for documento in documentos:
            documento["tipo"] = "documento"
        
        contenidos = ejercicios+links+textos+documentos   
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
def ejercicio(request):
    if (request.POST.get('id')):
        ejercicio = Ejercicio.objects.get(id = request.POST.get('id'))

        rol = Usuario_Curso.objects.get(usuario = request.user, curso = ejercicio.curso).tipo_subscripcion

        if (rol.nombre == "Alumno"):
            try:
                entrega = Entrega.objects.get(ejercicio = ejercicio.id, autor = request.user.id)
            except:
                entrega = False

            contexto = {
                "ejercicio": ejercicio,
                "entrega": entrega
            }

            return render(request, 'vroom/ejercicio_alumno.html', contexto)

        else:
            
            alumnos_curso = list(Usuario_Curso.objects.filter(curso = ejercicio.curso, tipo_subscripcion = Tipo_Subscripcion.objects.get(nombre = "Alumno").id).values())

            alumnos = []
            for alumno in alumnos_curso:
                id_alumno = alumno["usuario_id"]
                alumnos.append(model_to_dict(Usuario.objects.get(id = id_alumno)))
                
            contexto = {
                "ejercicio": model_to_dict(ejercicio),
                "alumnos": list(alumnos)
            }

            return render(request, 'vroom/ejercicio_profesor.html', contexto)