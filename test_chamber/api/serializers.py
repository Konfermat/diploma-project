from rest_framework import serializers
from .models import Step, StepElement, TextElement, TestElement, TestOption

# сделай сам

# --- СЕРИАЛИЗАТОРЫ КОНТЕНТА ---

class TextElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextElement
        fields = ['body']


class TestOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestOption
        fields = ['id', 'answer'] 


class TestElementSerializer(serializers.ModelSerializer):
    options = TestOptionSerializer(many=True, read_only=True)

    class Meta:
        model = TestElement
        fields = ['question', 'options']


# --- СЕРИАЛИЗАТОРЫ СТРУКТУРЫ ---

class StepElementSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = StepElement
        fields = ['id', 'order', 'step_element_type', 'content']

    def get_content(self, obj):
        if obj.step_element_type == 'TEXT' and hasattr(obj, 'text_content'):
            return TextElementSerializer(obj.text_content).data
        if obj.step_element_type == 'TEST' and hasattr(obj, 'test_content'):
            return TestElementSerializer(obj.test_content).data
        return None


class StepDetailSerializer(serializers.ModelSerializer):
    elements = StepElementSerializer(many=True, read_only=True)

    class Meta:
        model = Step
        fields = ['id', 'title', 'order', 'elements']
