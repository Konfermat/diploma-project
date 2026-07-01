from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views # Ваш привычный стиль импорта

urlpatterns = [
    # Авторизация (Вход) — возвращает access и refresh токены
    # TODO ОТСЛЕДИ ЧЕРТОВЫ NAME
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Обновление access-токена с помощью refresh-токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Регистрация нового пользователя
    path('register/', views.register_view, name='auth_register'),

    # Ваши старые URL-адреса уроков
    path('lessons/', views.lesson_list_view, name='lesson-list'),
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson-detail'),
    path('parts/<int:pk>/', views.lesson_part_detail_view, name='part-detail'),
    path('parts/submit-test/', views.submit_test_answer_view, name='submit-test'),

    # Профиль
    # пределано,
    # path('profile/', views.profile_view, name='user-profile'),
    path('profile/<int:pk>/', views.user_detail_view, name='user-detail'),

    
]
