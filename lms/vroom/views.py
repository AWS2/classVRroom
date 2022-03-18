from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Entrega

from .models import *


def entrega(request):
    return render(request, 'vroom/entrega.html')

def index(request):

    return render(request, 'vroom/index.html')