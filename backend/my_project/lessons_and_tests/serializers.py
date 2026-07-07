from rest_framework import serializers
from .models import (
    Lesson, 
    LessonPart, 
    Text, 
    Test, 
    TestOption, 
    User
    )


class TestOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestOption
        fields = ['id', 'answer', 'order']

class TestSerializer(serializers.ModelSerializer):
    options = TestOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'question', 'order', 'options']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'lesson_material', 'order']

# LESSON
class LessonPartDetailSerializer(serializers.ModelSerializer):
    texts = TextSerializer(many=True, read_only=True)
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = LessonPart
        fields = ['id', 'title', 'order', 'texts', 'tests']

class LessonPartShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPart
        fields = ['id', 'title', 'order']

class LessonListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    parts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'user', 'parts_count', 'is_published', 'created_at']

class LessonDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    parts = LessonPartDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'user', 'is_published', 'parts', 'created_at']



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'date_joined']
