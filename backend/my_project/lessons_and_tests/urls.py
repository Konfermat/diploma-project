from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views # Ваш привычный стиль импорта

urlpatterns = [
    # 1. Авторизация (Вход) — возвращает access и refresh токены
    # URL: http://127.0.0
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 2. Обновление access-токена с помощью refresh-токена
    # URL: http://127.0.0refresh/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 3. Регистрация нового пользователя
    # URL: http://127.0.0
    path('register/', views.register_view, name='auth_register'),

    # Ваши старые URL-адреса уроков
    path('lessons/', views.lesson_list_view, name='lesson-list'),
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson-detail'),
    path('parts/<int:pk>/', views.lesson_part_detail_view, name='part-detail'),
    path('parts/submit-test/', views.submit_test_answer_view, name='submit-test'),
]
