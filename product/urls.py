from django.urls import path
from .views import ProductListCreateView

urlpatterns = [
    path('products/<int:pk>/', ProductListCreateView.as_view(), name='product-detail'),
]