from django.urls import path
from product.views import ProductListCreateView, ProductCRUDView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductCRUDView.as_view(), name='product-detail'),
]