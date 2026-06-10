from django.urls import path
from . import views

urlpatterns = [
    # Курсы
    path('courses/', views.course_list, name='course-list'),
    path('courses/<int:pk>/', views.course_detail, name='course-detail'),  # Исправлено: заменен синтаксис и добавлен слэш
    
    # Сортировка шагов курса
    path('courses/<int:course_id>/reorder_steps/', views.reorder_steps, name='reorder-steps'),  # Исправлено: <int:course_id>
    
    # Шаги
    path('steps/', views.step_list, name='step-list'),
    
    # Сортировка и создание элементов внутри конкретного шага
    path('steps/<int:step_id>/reorder_elements/', views.reorder_elements, name='reorder-elements'),  # Исправлено: <int:step_id>
    path('steps/<int:step_id>/elements/create/', views.create_step_element, name='create-step-element'),  # Добавлено!
    
    # Списки элементов (вспомогательные/отладочные эндпоинты)
    path('step_elements/', views.step_element_list, name='step-element-list'),
    path('text_elements/', views.text_element_list, name='text-element-list'),
    path('test_elements/', views.test_element_list, name='test-element-list'),
]
