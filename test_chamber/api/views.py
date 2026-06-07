from django.shortcuts import get_object_or_404
from api.serializers import CourseSerializer, StepSerializer, StepElementSerializer, TextElementSerializer, TestElementSerializer
from api.models import Course, Step, StepElement, TextElement, TestElement

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(['GET'])
def step_list(request):
    steps = Step.objects.all()
    serializer = StepSerializer(steps, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def step_element_list(request):
    step_elements = StepElement.objects.all()
    serializer = StepElementSerializer(step_elements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def text_element_list(request):
    text_elements = TextElement.objects.all()
    serializer = TextElementSerializer(text_elements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def test_element_list(request):
    test_elements = TestElement.objects.all()
    serializer = TestElementSerializer(test_elements, many=True)
    return Response(serializer.data)


