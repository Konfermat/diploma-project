import random
from django.core.management.base import BaseCommand
from django.utils.lorem_ipsum import words, paragraphs 

from django.db import transaction

from lessons_and_tests.models import User, Test



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Начало заполнения базы данных...")

        # Получаем или создаем суперпользователя
        user, created = User.objects.get_or_create(username='admin')
        if created:
            user.set_password('1234')
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write("Создан новый суперпользователь 'admin' с паролем '1234'")

        # для возврата к прежним данным в случае ошибки
        with transaction.atomic():
            # Очищаем старые данные (опционально, если хотите обновлять БД с нуля)
            Test.objects.all().delete()            


            # Как создать один объект
            Test.objects.create(question=words(random.randint(3, 5), common=False))

        self.stdout.write("Конец заполнения базы данных")



                    
       