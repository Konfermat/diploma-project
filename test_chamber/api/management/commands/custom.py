from django.utils import lorem_ipsum
from django.core.management.base import BaseCommand
from api.models import Course


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(Course.objects)

# python shell commands

from api.models import Course, Step, User
from django.utils import lorem_ipsum

user = User.objects.filter(username='admin').first()
if not user:
    user = User.objects.create_superuser(username='admin', password='1234')


c1 = Course(title='Python One', description=lorem_ipsum.words(10, common=False), user=user)
c1.save()

s0 = Step(id=None, course=c1, title='Step Intro')
s0.save()