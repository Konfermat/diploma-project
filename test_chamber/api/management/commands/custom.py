from django.utils import lorem_ipsum
from django.core.management.base import BaseCommand
from api.models import Course


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        print(Course)
        def fixing(*args):
            seq = [obj.objects.all() for obj in args]

        fixing()