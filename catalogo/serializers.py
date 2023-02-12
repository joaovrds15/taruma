from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = [
            'pais',
            'nome',
            'descricao',
            'categories',
            'objectives',
            'image_url',
            'modo_uso',
        ]
        extra_kwargs = {
            'descricao': {'required': False},
            'conservacao': {'required': False},
            'sugestao_de_uso': {'required': False},
            'modo_de_uso': {'required': False},
        }
    
    def create(self, validated_data):
        categories = validated_data.pop('categories')
        product = Product.objects.create(**validated_data)
        product.categories.set(categories)
        return product
    