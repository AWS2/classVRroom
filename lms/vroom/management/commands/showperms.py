from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group , Permission
import logging

class Command(BaseCommand):
    def handle(self, *args, **option):
        perms = Permission.objects.all()
        logging.warning(format(perms))