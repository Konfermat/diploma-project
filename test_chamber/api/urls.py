from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list),
    path('steps/', views.step_list),
]