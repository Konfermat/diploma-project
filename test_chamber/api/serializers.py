from rest_framework import serializers
from .models import Course, User, Step

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'created_at',
        )



class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = (
            'id',
            'course',
            'title',
            'order',
        )


    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Порядковый номер не может быть ниже нуля.'
            )
        return value