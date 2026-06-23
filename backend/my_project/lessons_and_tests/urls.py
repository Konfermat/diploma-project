from django.urls import path
from . import views

urlpatterns = [
    # Для теста
    path('users/', views.user_list, name='user-list'),
]
