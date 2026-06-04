from django.shortcuts import get_object_or_404
from api.serializers import CourseSerializer, StepSerializer
from api.models import Course, Step

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def step_list(request):
    steps = Step.objects.all()
    serializer = StepSerializer(steps, many=True)
    return Response(serializer.data)


