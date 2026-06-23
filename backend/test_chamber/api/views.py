from django.shortcuts import get_object_or_404
from django.db import transaction  

from api.serializers import (
    CourseSerializer, StepSerializer, StepElementSerializer, 
    TextElementSerializer, TestElementSerializer, ReorderIdsSerializer, 
    StepElementCreateSerializer
)
from api.models import (Course, Step, StepElement, 
                        TextElement, TestElement, TestOption
)

from rest_framework import status  
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def course_title_list(request):
    titles = Course.objects.values_list('title', flat=True)
    return Response(list(titles))


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


# Протестируй
@api_view(['POST'])
def reorder_steps(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Курс не найден."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReorderIdsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ordered_ids = serializer.validated_data['ordered_ids']

    steps = Step.objects.filter(course=course, id__in=ordered_ids)

    if steps.count() != len(ordered_ids):
        return Response(
            {"error": "Переданы ID шагов, не принадлежащих данному курсу, или несуществующие ID."},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        steps_dict = {step.id: step for step in steps}
        updated_steps = []
        
        for index, step_id in enumerate(ordered_ids, start=1):
            step = steps_dict[step_id]
            step.order = index
            updated_steps.append(step)
        
        Step.objects.bulk_update(updated_steps, ['order'])

    return Response(
        StepSerializer(course.steps.all(), many=True).data, 
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def reorder_elements(request, step_id):
    try:
        step = Step.objects.get(pk=step_id)
    except Step.DoesNotExist:
        return Response({"error": "Шаг не найден."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReorderIdsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ordered_ids = serializer.validated_data['ordered_ids']

    elements = StepElement.objects.filter(step=step, id__in=ordered_ids)

    if elements.count() != len(ordered_ids):
        return Response(
            {"error": "Переданы ID элементов, не принадлежащих данному шагу."},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        elements_dict = {el.id: el for el in elements}
        updated_elements = []
        
        for index, el_id in enumerate(ordered_ids, start=1):
            element = elements_dict[el_id]
            element.order = index
            updated_elements.append(element)
            
        StepElement.objects.bulk_update(updated_elements, ['order'])

    return Response(
        StepSerializer(step).data, 
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def create_step_element(request, step_id):
    try:
        step = Step.objects.get(pk=step_id)
    except Step.DoesNotExist:
        return Response({"error": "Шаг не найден."}, status=status.HTTP_404_NOT_FOUND)

    serializer = StepElementCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    element_type = serializer.validated_data['type']
    content_data = serializer.validated_data['validated_content_data']

    with transaction.atomic():
        step_element = StepElement.objects.create(
            step=step,
            step_element_type=element_type
        )

        if element_type == 'TEXT':
            TextElement.objects.create(
                step_element=step_element, 
                body=content_data['body']
            )
            
        elif element_type == 'TEST':
            test_element = TestElement.objects.create(
                step_element=step_element,
                question=content_data['question']
            )
            options_data = content_data['options']
            for option in options_data:
                TestOption.objects.create(
                    test_element=test_element,
                    answer=option['answer'],
                    is_correct=option.get('is_correct', False)
                )

    return Response(
        {"message": "Элемент успешно создан", "id": step_element.id}, 
        status=status.HTTP_201_CREATED
    )
