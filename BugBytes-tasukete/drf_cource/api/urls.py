from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    # pk = primary key
    path('products/<int:pk>/', views.product_detail)
]