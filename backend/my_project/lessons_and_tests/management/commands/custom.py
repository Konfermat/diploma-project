from django.utils import lorem_ipsum
from django.core.management.base import BaseCommand
from lessons_and_tests.models import User, Test


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        
        # здесь буду примеры хранить 
        def test_info():
            def example1():
                # .first() возвращает объект
                tests = Test.objects.first()
                print(tests.question)

            def example2():
                # QuerySets
                tests = Test.objects.all()
                for i in tests:
                    print(i.id, i.question)

            
            # execution
            # example1()
            example2()



        # exe
        test_info()
        