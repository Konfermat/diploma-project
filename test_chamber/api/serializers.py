from rest_framework import serializers
from .models import Course, User, Step, StepElement, TextElement, TestElement

'''щитпост:
    hyperlink related field для указывания списках в таблицах для перехода по ним
    что твоя api должна вернуть? Ссылку или данные?
    Подумай какая логика должна быть именно у тебя
    для того чтобы переслать всю данные одним запросом передай данные
    если данные тяжелые то нужно сообразить с ссылками 

    сериализаторы их методы их вложенность а также есть еще generic сериализаторы которые не привязаны к таблицам

    serializers method нужен для вычислений данных полей
    serializers method можно переименовать через method_name

    если скрыть steps то будут показываться fk
    сделать вокруг этого логику?
    many=True проверь еще эту логику
'''

class TestOptionSerializer(serializers.ModelSerializer):
    pass # TODO две опции миимум

class TestElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestElement
        fields = (
            'step_element',
            'question',
        )

class TextElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextElement
        fields = (
            'step_element',
            'body',
        )

class StepElementSerializer(serializers.ModelSerializer):
    text_content = TextElementSerializer(read_only=True)
    test_content = TestElementSerializer(read_only=True)
    class Meta:
        model = StepElement
        fields = (
            'step',
            'step_element_type',
            'text_content',
            'test_content',
        )
    
    # TODO сделать валидацию типов

class StepSerializer(serializers.ModelSerializer):
    elements = StepElementSerializer(many=True, read_only=True)
    class Meta:
        model = Step
        fields = (
            'id',
            'course',
            'title',
            'order',
            'elements',
        )



class CourseSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'created_at',
            'steps',
        )

    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Порядковый номер не может быть ниже нуля.'
            )
        return value