from django.urls import path
from .views import ProductRetrieveUpdateDestroyView, ProductLikeAPIView, ProductUnlikeAPIView

urlpatterns = [
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('products/<int:product_id>/like/', ProductLikeAPIView.as_view(), name='product-likes'),
    path('products/<int:product_id>/unlike/', ProductUnlikeAPIView.as_view(), name='product-unlike'),
]