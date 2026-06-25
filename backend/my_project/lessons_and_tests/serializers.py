from rest_framework import serializers
from .models import Lesson, LessonPart, Text, Test, TestOption


# 1. СЕРИАЛИЗАТОР ВАРИАНТОВ ОТВЕТОВ
class TestOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestOption
        # Передаем id (нужен фронту для отправки POST-запроса) и текст варианта.
        # Поле is_correct ИСКЛЮЧЕНО из соображений безопасности (чтобы не подсмотрели в коде).
        fields = ['id', 'answer', 'order']


# 2. СЕРИАЛИЗАТОР ТЕСТОВ (Включает в себя варианты ответов)
class TestSerializer(serializers.ModelSerializer):
    # Подтягиваем связанные варианты ответов через related_name='options'
    options = TestOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'question', 'order', 'options']


# 3. СЕРИАЛИЗАТОР ТЕКСТОВ
class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'lesson_material', 'order']


# 4. СЕРИАЛИЗАТОР ДЕТАЛЕЙ ЧАСТИ УРОКА (Тексты + Тесты для центрального прямоугольника)
class LessonPartDetailSerializer(serializers.ModelSerializer):
    # Объединяем тексты и тесты внутри одной части урока через их related_name
    texts = TextSerializer(many=True, read_only=True)
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = LessonPart
        fields = ['id', 'title', 'order', 'texts', 'tests']


# 5. СЕРИАЛИЗАТОР ЧАСТЕЙ УРОКА ДЛЯ НАВИГАЦИИ (Компактный)
class LessonPartShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPart
        fields = ['id', 'title', 'order']


# 6. СЕРИАЛИЗАТОР ДЛЯ КАРТОЧКИ УРОКА (На главной странице)
class LessonListSerializer(serializers.ModelSerializer):
    # Выводим строковое имя автора вместо числового ID
    user = serializers.ReadOnlyField(source='created_by.username')
    # Поле подтянет значение из .annotate(parts_count=Count('parts')) во views.py
    parts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'user', 'parts_count', 'is_published', 'created_at']


# 7. СЕРИАЛИЗАТОР ДЕТАЛЕЙ УРОКА (Выдает метаданные урока + список его частей для меню)
class LessonDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    # Используем созданный выше компактный сериализатор частей
    parts = LessonPartShortSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'user', 'is_published', 'parts', 'created_at']

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    # Поле пароля делаем только для записи, чтобы оно не возвращалось в JSON
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Метод create_user автоматически хеширует пароль в базе данных
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
