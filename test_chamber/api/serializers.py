from rest_framework import serializers
from .models import Course, User, Step

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'created_at',
        ]

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = [
            'course',
            'title',
            'order',
        ]

