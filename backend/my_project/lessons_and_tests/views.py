from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Count 

from .models import Lesson, LessonPart, Test, TestOption, UserTestAnswer 

from .serializers import (
    LessonPartDetailSerializer, 
    RegisterSerializer, 
    LessonListSerializer, 
    LessonDetailSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Строго для авторизованных
def profile_view(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "date_joined": user.date_joined.strftime("%d.%m.%Y %H:%M")  # Красивый формат даты
    }, status=status.HTTP_200_OK)


# ПОЛУЧЕНИЕ КОНТЕНТА ЧАСТИ УРОКА (Функция)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def lesson_part_detail_view(request, pk):
    """
    Возвращает тексты и тесты для конкретной части урока.
    Сортировка внутри списков происходит автоматически благодаря Meta моделей.
    """
    # Оптимизируем запросы через prefetch_related, чтобы избежать проблемы N+1
    lesson_part = get_object_or_404(
        LessonPart.objects.prefetch_related('texts', 'tests__options'), 
        pk=pk
    )
    
    # Передаем объект в сериализатор и отдаем JSON
    serializer = LessonPartDetailSerializer(lesson_part)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ПРОВЕРКА ОТВЕТА НА ТЕСТ (Функция)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_test_answer_view(request):
    """
    Принимает ответ пользователя, сверяет is_correct на сервере
    и сохраняет/обновляет результат в истории.
    """
    test_id = request.data.get('test_id')
    option_id = request.data.get('option_id')

    # Валидация входных данных
    if not test_id or not option_id:
        return Response(
            {"error": "Необходимо передать test_id и option_id."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Проверяем существование теста и варианта в БД
    test = get_object_or_404(Test, pk=test_id)
    option = get_object_or_404(TestOption, pk=option_id, option=test)

    # Проверка правильности на бэкенде (безопасно для фронтенда)
    is_correct = option.is_correct

    # Записываем попытку (создаем новую или перезаписываем старую)
    user_answer, created = UserTestAnswer.objects.update_or_create(
        user=request.user,
        test=test,
        defaults={
            'chosen_option': option,
            'is_correct': is_correct
        }
    )

    # Формируем вердикт для фронтенда
    return Response({
        "is_correct": is_correct,
        "message": "Правильно!" if is_correct else "Неверно, попробуйте еще раз."
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny]) # Страницу со списком уроков могут видеть даже неавторизованные гости
def lesson_list_view(request):
    """
    Возвращает список всех опубликованных уроков для главной страницы.
    Уроки отсортированы: сначала новые (по дате создания).
    """
    # Оптимизация: 
    # 1. select_related('user') сразу подгружает авторов (избегаем N+1 для юзеров)
    # 2. annotate(parts_count=Count('parts')) считает количество частей прямо на уровне базы данных SQL
    lessons = Lesson.objects.filter(is_published=True)\
                            .select_related('created_by')\
                            .annotate(parts_count=Count('parts'))\
                            .order_by('-created_at')
    
    # Передаем список в сериализатор. Флаг many=True обязателен для коллекций!
    serializer = LessonListSerializer(lessons, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny]) # Список частей урока могут видеть все гости сайта
def lesson_detail_view(request, pk):
    """
    Возвращает информацию о конкретном уроке и список всех его частей 
    (только заголовки и ID) для отображения меню навигации.
    """
    # Получаем урок по ID и сразу подгружаем все связанные части (оптимизация)
    lesson = get_object_or_404(
        Lesson.objects.filter(is_published=True).prefetch_related('parts'),
        pk=pk
    )
    
    # Передаем объект в сериализатор
    serializer = LessonDetailSerializer(lesson)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([AllowAny]) # Регистрация доступна всем гостям
def register_view(request):
    """
    Регистрация нового пользователя в системе.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Пользователь успешно зарегистрирован!"}, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
