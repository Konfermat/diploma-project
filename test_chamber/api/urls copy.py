from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list),
    path('courses/<int:pk>', views.course_detail),
    # Сортировка шагов курса (передаем id курса)
    path('courses/<int=course_id>/reorder_steps/', views.reorder_steps, name='reorder-steps'),
    path('steps/', views.step_list),
    # Сортировка элементов внутри шага (передаем id шага)
    path('steps/<int=step_id>/reorder_elements/', views.reorder_elements, name='reorder-elements'),
    path('step_elements/', views.step_element_list),
    path('text_elements/', views.text_element_list),
    path('test_elements/', views.test_element_list),
]
