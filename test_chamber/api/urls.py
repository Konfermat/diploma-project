from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list),
    path('courses/<int:pk>', views.course_detail),
    path('steps/', views.step_list),
    path('step_elements/', views.step_element_list),
    path('text_elements/', views.text_element_list),
    path('test_elements/', views.test_element_list),
]