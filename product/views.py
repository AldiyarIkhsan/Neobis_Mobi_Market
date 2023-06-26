from rest_framework.views import APIView
from product.models import Product, ProductLike
from product.serializers import ProductSerializer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = permissions.IsAuthenticated

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = permissions.IsAuthenticated

class ProductLikeAPIView(APIView):
    permission_classes = permissions.IsAuthenticated

    def post(self, request, product_id):
        user = request.user
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if product.likes.filter(id=user.id).exists():
            return Response({'message': 'You have already liked this product'}, status=status.HTTP_400_BAD_REQUEST)

        ProductLike.objects.create(product=product, user=user)

        return Response({'message': 'Product liked successfully'}, status=status.HTTP_201_CREATED)


class ProductUnlikeAPIView(APIView):
    permission_classes = permissions.IsAuthenticated

    def delete(self, request, product_id):
        user = request.user
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if not product.likes.filter(id=user.id).exists():
            return Response({'message': 'You have not liked this product'}, status=status.HTTP_400_BAD_REQUEST)

        ProductLike.objects.filter(product=product, user=user).delete()

        return Response({'message': 'Product unliked successfully'}, status=status.HTTP_204_NO_CONTENT)