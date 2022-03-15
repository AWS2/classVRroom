from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def entrega(request):
    return render(request, 'vroom/entrega.html')