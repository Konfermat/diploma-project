import random
from django.core.management.base import BaseCommand
from django.utils.lorem_ipsum  import words, paragraphs 

from django.db import transaction

from api.models import User, Course, Step, StepElement, TextElement, TestElement, TestOption


class Command(BaseCommand):
    help = 'Команда для автоматического заполнения БД тестовыми курсами, шагами и полиморфным контентом'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начало заполнения базы данных...")

        # 1. Получаем или создаем суперпользователя
        user, created = User.objects.get_or_create(username='admin')
        if created:
            user.set_password('1234')
            user.is_superuser = True
            user.is_staff = True
            user.save()
            # Обрати внимание
            self.stdout.write("Создан новый суперпользователь 'admin' с паролем '1234'")

        # Оборачиваем генерацию в одну транзакцию, чтобы всё создавалось быстро и безопасно
        # Обрати внимание 
        with transaction.atomic():
            
            # Очищаем старые данные (опционально, если хотите обновлять БД с нуля)
            Course.objects.all().delete()

            # 2. Создаем курсы
            courses_to_create = [
                Course(
                    title='Поколение Python', 
                    description='В курсе рассказывается об основных типах данных, конструкциях и принципах структурного программирования языка Python. Курс содержит теорию в формате текстовых конспектов и более 500 задач с автоматизированной проверкой.',
                    user=user
                ),
                Course(
                    title='Продвинутый Django', 
                    description='Изучаем глубокие архитектурные концепции: полиморфные связи, кастомные менеджеры, оптимизацию ORM-запросов и работу с транзакциями.',
                    user=user
                )
            ]
            Course.objects.bulk_create(courses_to_create)
            
            # Получаем созданные курсы из базы
            courses = Course.objects.all()

            # 3. Наполняем каждый курс шагами и элементами
            for course in courses:
                # Генерируем от 3 до 5 шагов для каждого курса
                for step_num in range(1, random.randint(4, 6)):
                    step = Step.objects.create(
                        course=course,
                        title=f"Урок {step_num}: " + words(2, common=False).capitalize(),
                        order=step_num
                    )

                    # 4. Внутри каждого шага создаем контент (текст и тесты попеременно)
                    for el_num in range(1, 4):
                        # Чередуем тип элемента
                        el_type = 'TEXT' if el_num % 2 != 0 else 'TEST'
                        
                        step_element = StepElement.objects.create(
                            step=step,
                            step_element_type=el_type,
                            order=el_num
                        )

                        if el_type == 'TEXT':
                            # Создаем текстовый блок
                            TextElement.objects.create(
                                step_element=step_element,
                                body=f"### Теория к уроку\n\n" + "\n\n".join(paragraphs(2, common=False))
                            )
                        
                        elif el_type == 'TEST':
                            # Создаем вопрос
                            test_element = TestElement.objects.create(
                                step_element=step_element,
                                question=f"Вопрос по теме урока: Сколько будет {random.randint(2, 5)} + {random.randint(2, 5)}?"
                            )
                            
                            # Создаем варианты ответов
                            TestOption.objects.create(test_element=test_element, answer="Правильный ответ", is_correct=True)
                            TestOption.objects.create(test_element=test_element, answer="Неправильный вариант А", is_correct=False)
                            TestOption.objects.create(test_element=test_element, answer="Неправильный вариант Б", is_correct=False)

        self.stdout.write(self.style.SUCCESS("База данных успешно наполнена тестовыми данными!"))
