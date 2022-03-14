from django.shortcuts import get_object_or_404, render

from django.contrib.auth.models import User
from .models import Entrega, Ejercicio, Curso

def entrega(request, id_ejercicio):
    entrega = get_object_or_404(Entrega, pk=id_ejercicio)
    ejercicio = get_object_or_404(Ejercicio, pk=entrega.ejercicio.id)
    curso = get_object_or_404(Curso, pk=ejercicio.curso.id)
    alumno = get_object_or_404(User, pk=entrega.autor.id)
    return render(request, 'vroom/entrega.html', {'entrega': entrega, 'ejercicio': ejercicio, 'curso': curso, 'alumno': alumno})