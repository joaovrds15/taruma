from rest_framework import serializers
from .models import Product, Category, Country
from rest_framework.views import exception_handler
from rest_framework.response import Response


class ProductSerializer(serializers.ModelSerializer):
    pais = serializers.CharField()
    class Meta:
        model = Product
        fields = [
            'id',
            'pais',
            'nome',
            'descricao',
            'conservacao',
            'sugestao_de_uso',
            'categories',
            'objectives',
            'image_url',
            'modo_uso',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            "objectives": {"required": False},
            "image_url": {"required": False},
            "modo_uso": {"required": False}
        }

    def validate(self, data):
        pais = Country.objects.filter(nome=data['pais'])
        if not pais.exists():
            raise serializers.ValidationError('Country name not found')
        if Product.objects.filter(nome=data['nome'], pais=pais[0].id).exists():
            raise serializers.ValidationError('Product already exists')
        return data

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        pais_nome = validated_data.pop('pais')
        pais = Country.objects.get(nome=pais_nome)
        validated_data['pais'] = pais
        product = Product.objects.create(**validated_data)
        for category in categories:
            category = Category.objects.get(id=category.id)
            product.categories.add(category)
        return product

