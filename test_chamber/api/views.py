from django.shortcuts import get_object_or_404
from api.serializers import CourseSerializer
from api.models import Course

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


