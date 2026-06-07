# сделать через Factory Boy но сначала сделать вручную по образу и подобию BugBytes

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum 
from api.models import User, Course, Step, StepElement, TextElement, TestElement, TestOption, UserStepProgress

import random
# random(randint(15))


class Command(BaseCommand):
    help = 'базовое заполнение таблиц'
    def handle(self, *args, **kwargs):
        # получаем пользователя
        user = User.objects.filter(username='admin').first()
        # если нету то создаем нового
        if not user:
            user = User.objects.create_superuser(username='admin', password='1234')

        # список на создание     
        courses = [
            Course(title='Поколение Python', 
            description='​В курсе рассказывается об основных типах данных, конструкциях и принципах структурного программирования языка Python. Курс содержит теорию в формате текстовых конспектов и более 500 задач с автоматизированной проверкой. Этот курс является первой частью линейки курсов "Поколение Python".',
            user=user,
            ),
            Course(title='Поколение Lorem', description=lorem_ipsum.words(100, common=False), user=user),
            Course(title='Поколение Ipsum', description=lorem_ipsum.words(100, common=False), user=user),
            ]
        # Создание по списку выше
        Course.objects.bulk_create(courses)
        courses = Course.objects.all()

        for course in courses:
            cnt = 1
            for i in range(random.randint(10, 15)):
                Step.objects.create(course=course, title=lorem_ipsum.words(2, common=False), order=cnt)
                cnt += 1


        
