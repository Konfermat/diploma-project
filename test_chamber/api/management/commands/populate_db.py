# сделать через Factory Boy но сначала сделать вручную по образу и подобию BugBytes


# для команды python manage.py populate_db
# чтобы это работало нужно:
    # создать management/commands/__init__.py
    # создать management/commands/your_custom_command_name.py
from django.core.management.base import BaseCommand

# how to lorem_ipsum
    # common=True(defalt) means it starts with classic lorem ipsum paragraph all the time
    # lorem_ipsum.paragraphs(count, common=True)
    # lorem_ipsum.sentence()
    # lorem_ipsum.words(count, common=False) # сгенерирует 5 рандомных латинских слов 
from django.utils import lorem_ipsum 
from api.models import User, Course, Step, StepElement, TextElement, TestElement, TestOption, UserStepProgress


class Command(BaseCommand):
    help = 'базовое заполнение таблиц'
    def handle(self, *args, **kwargs):
        # получаем пользователя
        user = User.objects.filter(username='admin').first()
        # если нету то создаем нового
        if not user:
            user = User.objects.create_superuser(username='admin', password='1234')
            
        courses = [
            Course(title='Поколение Python', 
            description='​В курсе рассказывается об основных типах данных, конструкциях и принципах структурного программирования языка Python. Курс содержит теорию в формате текстовых конспектов и более 500 задач с автоматизированной проверкой. Этот курс является первой частью линейки курсов "Поколение Python".',
            user=user,
            ),
            Course(title='Поколение Lorem', description=lorem_ipsum.words(100, common=False), user=user),
            Course(title='Поколение Ipsum', description=lorem_ipsum.words(100, common=False), user=user),
            ]
        # Создание нескольких
        Course.objects.bulk_create(courses)
        courses = Course.objects.all()
        



# Создает один
# Order.objects.create(user=user)

# создает несколько по списку
# Course.objects.bulk_create(courses)
# courses = 
#