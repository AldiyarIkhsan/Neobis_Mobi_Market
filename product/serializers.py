from rest_framework import serializers
from authentication.models import User
from .models import Product

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username')

class ProductSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    likes = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ["id", "like_count", "name", "price", "photo", "description", "orderer", "likes"]
        read_only_fields = ('id', 'orderer', 'like_count')

    def get_like_count(self, obj):
        return obj.like_count


