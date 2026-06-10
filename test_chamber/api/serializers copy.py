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
    class Meta:
        model = TestOption
        fields = [
            'answer', 
            'is_correct'
        ]

class TestElementSerializer(serializers.ModelSerializer):
    options = TestOptionSerializer(many=True)
    class Meta:
        model = TestElement
        fields = [
            'question', 
            'options'
        ]

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
            'id'
            'step',
            'order',
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

# Фабричный сериализатор создания
class StepElementCreateSerializer(serializers.ModelSerializer):
    # Используем ваши типы: TEXT и TEST
    type = serializers.ChoiceField(choices=['TEXT', 'TEST'], write_only=True)
    content_data = serializers.JSONField(write_only=True)

    class Meta:
        model = StepElement
        fields = ['id', 'step', 'type', 'content_data', 'order']
        extra_kwargs = {
            'step': {'required': False},
            'order': {'required': False}
        }

    def validate(self, attrs):
        element_type = attrs.get('type')
        content_data = attrs.get('content_data')

        if element_type == 'TEXT':
            serializer = TextElementSerializer(data=content_data)
        elif element_type == 'TEST':
            serializer = TestElementSerializer(data=content_data)
        else:
            raise serializers.ValidationError({"type": "Неизвестный тип контента."})

        serializer.is_valid(raise_exception=True)
        attrs['validated_content_data'] = serializer.validated_data
        return attrs

class CourseDetailSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'steps',
        )

class RecorderIdsSerializer(serializers.ModelSerializer):
    # Принимает массив id: {"ordered_ids": [1, 2, 3]}
    # Спросить как это работает?
    ordered_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text='Список ID в новом порядке отображения.'
    )
    def validate_ordered_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError('Список ID содержит дубликаты.')
        return value



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