import factory
from catalogo.models import *

class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    nome = factory.Faker('country')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    nome = factory.Faker('word')

class ObjectiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Objective

    nome = factory.Faker('word')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    pais = factory.SubFactory(CountryFactory)
    nome = factory.Faker('word')
    descricao = "Product description"
    conservacao = "Product conservation"
    sugestao_de_uso = "Product usage suggestion"
    image_url = "http://example.com/image.png"
    modo_uso = "Product usage"