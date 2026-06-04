from django.core.management.base import BaseCommand
from api.models import Course


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(Course.objects)