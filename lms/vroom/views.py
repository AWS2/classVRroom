from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
def entrega(request):
    return render(request, 'vroom/entrega.html')
