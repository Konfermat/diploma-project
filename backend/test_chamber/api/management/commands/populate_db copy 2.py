

            
# Создает один
# Order.objects.create(user=user)

# создает несколько по списку
# Course.objects.bulk_create(courses)


# сделать через Factory Boy но сначала сделать вручную по образу и подобию BugBytes

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum 
from api.models import User, Course, Step, StepElement, TextElement, TestElement, TestOption, UserStepProgress

import random
# random(randint(15))


class Command(BaseCommand):
    help = 'базовое заполнение таблиц'
    def handle(self, *args, **kwargs):

        def get_superuser():
            # получаем пользователя
            user = User.objects.filter(username='admin').first()
            # если нету то создаем нового
            if not user:
                user = User.objects.create_superuser(username='admin', password='1234')
                return user
            return user

        def populate_courses_steps():
            user = get_superuser()
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
            # сбор курсов
            courses = Course.objects.all()

            for course in courses:
                cnt = 1
                for i in range(random.randint(10, 15)):
                    Step.objects.create(course=course, title=lorem_ipsum.words(2, common=False), order=cnt)
                    cnt += 1
        # populate_courses_steps()
        
        def populate_step_elements():
            steps = Step.objects.all()
                # создаем тип
            StepElement.objects.create(step=steps[0], step_element_type='text')
        # populate_step_elements()
        def populate_wrong_type():
            steps = Step.objects.all()
            StepElement.objects.create(step=steps[0], step_element_type='teext')
        # populate_wrong_type()

        def del_wrong_type():
            temp = StepElement.objects.filter(step_element_type='teext').first()
            temp.delete()
        # del_wrong_type()
        def populate_text_element():
            # нужно класть объект а не QuerySet
            step_element = StepElement.objects.filter(step=1).first()
            TextElement.objects.create(step_element=step_element, body=lorem_ipsum.words(15, common=False))
        # populate_text_element()
        def populate_step_with_text_element():
            step = Step.objects.filter(title='quae beatae').first()
            StepElement.objects.create(step=step, step_element_type='test')
        # populate_step_with_text_element()
        def populate_test_element():
            step_element = StepElement.objects.filter(step_element_type='test').first()
            TestElement.objects.create(step_element=step_element, question=lorem_ipsum.words(5))
        # populate_test_element()


            
            
            
        


            
# Создает один
# Order.objects.create(user=user)

# создает несколько по списку
# Course.objects.bulk_create(courses)

# вернет объект поля которых можно вызвать
# StepElement.objects.filter(step_element_type='teext').first()
# Вернет QuerySet нужен хз зачем. Забыл
# StepElement.objects.filter(step_element_type='teext')
