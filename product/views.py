from rest_framework.views import APIView
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework import status, generics, permissions
from drf_yasg.utils import swagger_auto_schema

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = permissions.IsAuthenticated
    @swagger_auto_schema(
        operation_description="This endpoint return all user products.",
        responses={
            200: ProductSerializer,
            400: 'Bad Request'
        }
    )

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class Product_CRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = permissions.IsAuthenticated
    @swagger_auto_schema(
        operation_description="This endpoint makes CRUD for product.",
        responses={
            200: ProductSerializer,
            400: 'Bad Request'
        }
    )