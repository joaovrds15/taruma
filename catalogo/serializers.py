from rest_framework import serializers
from .models import *
from rest_framework.views import exception_handler
from rest_framework.response import Response
import json


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'nome')


class ProductSerializer(serializers.ModelSerializer):
    pais = serializers.CharField()
    categories = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True)
    objectives = serializers.ListField(
        child=serializers.CharField(max_length=100),write_only=True , required=False)

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

    def validate_pais(self, value):
        pais = Country.objects.filter(nome=value)
        if not pais.exists():
            raise serializers.ValidationError('Country name not found')
        return value


    def validate_categories(self, values):
        for category in values:
            if not Category.objects.filter(nome=category).exists():
                raise serializers.ValidationError(
                    'Category ' + category + ' not found')
        return values

    def validate_objectives(self, values):
        for objective in values:
            if not Objective.objects.filter(nome=objective).exists():
                raise serializers.ValidationError(
                    'Objective ' + objective + ' not found')
        return values

    def validate(self, data):
        pais = Country.objects.filter(nome=data['pais'])
        if not pais.exists():
            raise serializers.ValidationError('Country name not found')
        if Product.objects.filter(nome=data['nome'], pais=pais[0].id).exists():
            raise serializers.ValidationError('Product already exists')
        return data

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        pais_nome = validated_data.get('pais')
        objectives = validated_data.pop('objectives') if validated_data.get('objectives') != None else validated_data.get('objectives')
        pais = Country.objects.get(nome=pais_nome)
        validated_data['pais'] = pais
        product = Product.objects.create(**validated_data)
        for category in categories:
            category_query = Category.objects.get(nome=category).id
            product.categories.add(category_query)
        if objectives != None:
            for objective in objectives:
                objective_query = Objective.objects.get(nome=objective)
                product.objectives.add(objective_query)
        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories')
        pais_nome = validated_data.get('pais')
        objectives = validated_data.pop('objectives') if validated_data.get('objectives') != None else validated_data.get('objectives')
        pais = Country.objects.get(nome=pais_nome)
        validated_data['pais'] = pais
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        for category in categories:
            category_query = Category.objects.get(nome=category).id
            instance.categories.add(category_query)
        if objectives != None:
            for objective in objectives:
                objective_query = Objective.objects.get(nome=objective)
                instance.objectives.add(objective_query)
        return instance
    
    def format_category(self, product):
        categoriesList = list()
        for category in product.categories.all():
            categoryDict = {'nome' : category.nome}
            categoriesList.append(categoryDict)
        return categoriesList
    
    def format_objectives(self, product):
        objectiveList = list()
        for objective in product.objectives.all():
            objectiveDict = {'nome' : objective.nome}
            objectiveList.append(objectiveDict)
        return objectiveList


    def format_response_list_all(self, products):
        response = []
        for product in products:
            productDict = {
                'nome' : product.nome,
                'pais' : product.pais.nome,
                'descricao' : product.descricao,
                'conservacao' : product.conservacao,
                'sugestao_de_uso' : product.sugestao_de_uso,
                'image_url' : product.image_url,
                'modo_uso' : product.modo_uso,
                'categories' : self.format_category(product),
                'objectives' : self.format_objectives(product),
            }
            response.append(productDict)
        return response

    def format_response_list_one(self, product):
        productDict = {
            'nome' : product.nome,
            'pais' : product.pais.nome,
            'descricao' : product.descricao,
            'conservacao' : product.conservacao,
            'sugestao_de_uso' : product.sugestao_de_uso,
            'image_url' : product.image_url,
            'modo_uso' : product.modo_uso,
            'categories' : self.format_category(product),
            'objectives' : self.format_objectives(product),
        }
        return productDict
            
