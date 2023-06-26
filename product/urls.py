from django.urls import path
from .views import ProductListCreateView, Product_CRUDView

urlpatterns = [
    path('products/<int:pk>/', ProductListCreateView.as_view(), name='product-detail'),
    path('products-crud', Product_CRUDView.as_view(), name='product-crud-view'),
]