from django.utils import lorem_ipsum
from django.core.management.base import BaseCommand
from api.models import Course, Step, StepElement, TextElement, TestElement


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        def fixing(*args):
            seq = [obj.objects.all() for obj in args]
            for i in seq:
                for j in i:
                    print(j.id)

        # fixing(Course, Step, StepElement)
    
        def fixing1():
            tmp = StepElement.objects.all()
            print(tmp)
        # print(fixing1())

        # Если данных мало и их не жалко, можно просто все удалить:
        StepElement.objects.all().delete()

        # Если данные нужны, сделаем order уникальным для каждого step_id: