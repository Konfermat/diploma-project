from django.shortcuts import render
from django.db import transaction

from lessons_and_tests.models import User

from lessons_and_tests.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

    