
from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group , Permission
from vroom.models import *
import logging

GROUPS = {
    'admin_centro': {
        "curso" : ["add","delete","change","view"],
        "documento" : ["add","delete","change","view"],
        "ejercicio" : ["add","delete","change","view"],
        "entrega" : ["add","delete","change","view"],
        "invitacion" : ["add","delete","change","view"],
        "link" : ["add","delete","change","view"],
        "texto" : ["add","delete","change","view"],
        "user" : ["add","delete","change","view"],
    },
    'profesores': {
        "documento" : ["add","delete","change","view"],
        "ejercicio" : ["add","delete","change","view"],
        "entrega" : ["add","delete","change","view"],
        "invitacion" : ["add","delete","change","view"],
        "link" : ["add","delete","change","view"],
        "texto" : ["add","delete","change","view"],
    }
}

class Command(BaseCommand):

    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):

        for group_name in GROUPS:   
            new_group, created = Group.objects.get_or_create(name=group_name)
    
            # Loop models in group
            for app_model in GROUPS[group_name]:

                # Loop permissions in group/model
                for permission_name in GROUPS[group_name][app_model]:

                    # Generate permission name as Django would generate it
                    name = "Can {} {}".format(permission_name, app_model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)
        Tipo_Subscripcion.objects.get_or_create(nombre="alumno")
        Tipo_Subscripcion.objects.get_or_create(nombre="profesor")
        Tipo_Ejercicio.objects.get_or_create(nombre="vr", icono="static/assets/archivos/vr.png")
        Tipo_Ejercicio.objects.get_or_create(nombre="no vr", icono="static/assets/archivos/novr.png")