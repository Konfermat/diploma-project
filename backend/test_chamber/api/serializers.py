from rest_framework import serializers
from .models import Course, User, Step, StepElement, TextElement, TestElement, TestOption


class TestOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestOption
        fields = (
            'answer', 
            'is_correct'
        )


class TestElementSerializer(serializers.ModelSerializer):
    options = TestOptionSerializer(many=True)

    class Meta:
        model = TestElement
        fields = (
            'question', 
            'options'
        )


class TextElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextElement
        fields = (
            'body',
        )


class StepElementSerializer(serializers.ModelSerializer):
    text_content = TextElementSerializer(read_only=True)
    test_content = TestElementSerializer(read_only=True)

    class Meta:
        model = StepElement
        fields = (
            'id',
            'step',
            'order',
            'step_element_type',
            'text_content',
            'test_content',
        )


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
# Изменено: наследуемся от serializers.Serializer, так как мы не сохраняем эту модель напрямую
class StepElementCreateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['TEXT', 'TEST'], write_only=True)
    content_data = serializers.JSONField(write_only=True)

    def validate(self, attrs):
        element_type = attrs.get('type')
        content_data = attrs.get('content_data')

        # 4. Исправлено: валидируем входящий JSON под конкретный тип контента
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
class CourseTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title'
        )


# Наследуемся от обычного Serializer, так как валидируем просто абстрактный JSON с фронтенда
class ReorderIdsSerializer(serializers.Serializer):
    ordered_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text='Список ID в новом порядке отображения.'
    )

    def validate_ordered_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError('Список ID содержит дубликаты.')
        return value
