import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import *
from catalogo.models import *


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.mark.django_db
def test_create_product_with_valid_data(api_client):
    Category.objects.create(nome='CategoriaTeste')
    Country.objects.create(nome='PaisTeste')
    Objective.objects.create(nome='Teste')
    url = reverse('create_product')
    data = {
        "pais" : "PaisTeste",
        "nome" : "ProdutoTeste",
        "descricao" : "Testando produto",
        "conservacao" : "na geladeria",
        "sugestao_de_uso" : "comer rapido",
        "categories" : ["CategoriaTeste"],
        "objectives" : ["Teste"],
        "image_url" : "https://testeimage.png",
        "modo_uso" : "comer com açúcar",
    }
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert "product_id" in message

@pytest.mark.django_db
def test_create_product_with_valid_data_and_not_required_fields(api_client):
    Category.objects.create(nome='CategoriaTeste')
    Country.objects.create(nome='PaisTeste')
    url = reverse('create_product')
    data = {
        "pais" : "PaisTeste",
        "nome" : "ProdutoTeste",
        "descricao" : "Testando produto",
        "conservacao" : "na geladeria",
        "sugestao_de_uso" : "comer rapido",
        "categories" : ["CategoriaTeste"]
    }
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert "product_id" in message

@pytest.mark.django_db
def test_create_product_duplicated(api_client):
    Category.objects.create(nome='CategoriaTeste')
    Country.objects.create(nome='PaisTeste')
    url = reverse('create_product')
    data = {
        "pais" : "PaisTeste",
        "nome" : "ProdutoTeste",
        "descricao" : "Testando produto",
        "conservacao" : "na geladeria",
        "sugestao_de_uso" : "comer rapido",
        "categories" : ["CategoriaTeste"]
    }
    api_client.post(url, data=data, format='json')
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert "Product already exists" in message
    assert response.status_code == 400

# @pytest.mark.django_db
# def test_list_products(api_client):
#     data = {
#         "pais" : "PaisTeste",
#         "nome" : "ProdutoTeste",
#         "descricao" : "Testando produto",
#         "conservacao" : "na geladeria",
#         "sugestao_de_uso" : "comer rapido",
#     }
#     Category.objects.create(nome='CategoriaTeste')
#     Country.objects.create(nome='PaisTeste')
#     product = Product.objects.create(
#         nome=data['nome'],
#         pais=data['PaisTeste'],
#         descricao=data['descricao'],
#         conservacao=data['conservacao'],
#         sugestao_de_uso=data['sugestao_de_uso']
#     )
#     product.categories.add('CategoriaTeste')
#     url = reverse('list_products')
#     response = api_client.get(url)

@pytest.mark.django_db
def test_update_product_with_valid_data(api_client):
    data = {
        "nome" : "ProdutoTeste",
        "descricao" : "Testando produto",
        "conservacao" : "na geladeria",
        "sugestao_de_uso" : "comer rapido",
        "image_url" : "https://testeimage.png",
        "modo_uso" : "comer com açúcar",
    }
    Category.objects.create(nome='CategoriaTeste')
    Country.objects.create(nome='PaisTeste')
    Objective.objects.create(nome='Teste')
    product = Product(**data)
    product.pais = Country.objects.get(nome='PaisTeste')
    category = Category.objects.get(nome='CategoriaTeste')
    product.save()
    dataAfter = {
        "pais" : "PaisTeste",
        "nome" : "ProdutoTesti",
        "descricao" : "Testando produto",
        "conservacao" : "na geladeria",
        "sugestao_de_uso" : "comer rapido",
        "image_url" : "https://testeimage.png",
        "modo_uso" : "comer com açúcar",
        "categories" : ["CategoriaTeste"]
    }
    product.categories.add(category)
    productBefore = Product.objects.get(nome=data['nome'])
    url = reverse('update_product', args=[product.id])
    response = api_client.put(url, data=dataAfter)
    productAfter = Product.objects.get(nome=dataAfter['nome'])
    message = response.content.decode('utf-8')
    assert productBefore.nome == data['nome']
    assert productAfter.nome == dataAfter['nome']