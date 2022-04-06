
from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group , Permission
from vroom.models import *
import logging

GROUPS = {
    'admin centro': {
        "curso" : ["add","delete","change","view"],
        "documento" : ["add","delete","change","view"],
        "tarea" : ["add","delete","change","view"],
        "auto_ puntuacion" : ["add","delete","change","view"],
        "entrega" : ["add","delete","change","view"],
        "invitacion" : ["add","delete","change","view"],
        "link" : ["add","delete","change","view"],
        "texto" : ["add","delete","change","view"],
        "user" : ["add","delete","change","view"],
        "usuario_ curso" : ["add","delete","change","view"],
    },
    'profesor': {
        "curso" : ["change","view"],
        "documento" : ["add","delete","change","view"],
        "tarea" : ["add","delete","change","view"],
        "entrega" : ["view"],
        "auto_ puntuacion" : ["view"],
        "invitacion" : ["add","delete","change","view"],
        "link" : ["add","delete","change","view"],
        "texto" : ["add","delete","change","view"],
        "usuario_ curso": ["add","delete","change","view"],
    }
}

class Command(BaseCommand):

    help = "Creates groups with its permissions and inserts essential data"

    def handle(self, *args, **options):

        admin_centro = Group.objects.filter(name = "admin centro")
        if not len(admin_centro) == 0:
            GROUPS.pop("admin centro")

        profesor = Group.objects.filter(name = "profesor")
        if not len(profesor) == 0:
            GROUPS.pop("profesor")

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

        

        Tipo_Subscripcion.objects.get_or_create(nombre="Alumno")
        Tipo_Subscripcion.objects.get_or_create(nombre="Profesor")