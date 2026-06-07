from rest_framework import serializers
from .models import Course, User, Step

# hyperlink related field для указывания списках в таблицах для перехода по ним
# что твоя api должна вернуть? Ссылку или данные?
# Подумай какая логика должна быть именно у тебя
# для того чтобы переслать всю данные одним запросом передай данные
# если данные тяжелые то нужно сообразить с ссылками 

# сериализаторы их методы их вложенность а также есть еще generic сериализаторы которые не привязаны к таблицам



class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = (
            'id',
            'course',
            'title',
            'order',
        )

class CourseSerializer(serializers.ModelSerializer):
    # serializers method нужен для вычислений данных полей
    # serializers method можно переименовать через method_name

    # если скрыть steps то будут показываться fk
    # сделать вокруг этого логику?
    # many=True проверь еще эту логику
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