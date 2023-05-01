import pytest
from catalogo.test.factories.product import *
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from pytest_django.asserts import *
from catalogo.models import *
from tests.support.assertion import assert_valid_schema
import json


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_create_product_with_valid_data(api_client):
    category = CategoryFactory.create()
    pais = CountryFactory.create()
    objective = ObjectiveFactory.create()
    product_data = ProductFactory.build()

    data = {
        'pais': pais.nome,
        'nome': product_data.nome,
        'descricao': product_data.descricao,
        'conservacao': product_data.conservacao,
        'sugestao_de_uso': product_data.sugestao_de_uso,
        'categories': [category.nome],
        'objectives': [objective.nome],
        'image_url': product_data.image_url,
        'modo_uso': product_data.modo_uso,
    }
    url = reverse('create_product')
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert "product_id" in message


@pytest.mark.django_db
def test_create_product_with_valid_data_and_not_required_fields(api_client):
    category = CategoryFactory.create()
    pais = CountryFactory.create()
    product_data = ProductFactory.build()
    data = {
        'pais': pais.nome,
        'nome': product_data.nome,
        'descricao': product_data.descricao,
        'conservacao': product_data.conservacao,
        'sugestao_de_uso': product_data.sugestao_de_uso,
        'categories': [category.nome],
        'image_url': product_data.image_url,
        'modo_uso': product_data.modo_uso,
    }
    url = reverse('create_product')
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert "product_id" in message


@pytest.mark.django_db
def test_create_product_duplicated(api_client):
    category = CategoryFactory.create()
    objective = ObjectiveFactory.create()
    product_data = ProductFactory.create()
    product_data.categories.add(category)
    data = {
        'pais': product_data.pais.nome,
        'nome': product_data.nome,
        'descricao': product_data.descricao,
        'conservacao': product_data.conservacao,
        'sugestao_de_uso': product_data.sugestao_de_uso,
        'categories': [category.nome],
        'objectives': [objective.nome],
        'image_url': product_data.image_url,
        'modo_uso': product_data.modo_uso,
    }
    url = reverse('create_product')
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    assert "Product already exists" in message
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_product_when_category_doesnt_exists(api_client):
    product_data = ProductFactory.build()
    pais = CountryFactory.create()
    category = CategoryFactory.create()
    data = {
        'pais': pais.nome,
        'nome': product_data.nome,
        'descricao': product_data.descricao,
        'conservacao': product_data.conservacao,
        'sugestao_de_uso': product_data.sugestao_de_uso,
        'categories': [category.nome, 'Iventado'],
        'image_url': product_data.image_url,
        'modo_uso': product_data.modo_uso,
    }
    url = reverse('create_product')
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    expected_message = "Category Iventado not found"
    assert expected_message in message
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_product_when_country_doesnt_exists(api_client):
    product_data = ProductFactory.build()
    category = CategoryFactory.create()
    data = {
        'pais': 'Iventado',
        'nome': product_data.nome,
        'descricao': product_data.descricao,
        'conservacao': product_data.conservacao,
        'sugestao_de_uso': product_data.sugestao_de_uso,
        'categories': [category.nome],
        'image_url': product_data.image_url,
        'modo_uso': product_data.modo_uso,
    }
    url = reverse('create_product')
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    expected_message = 'Country name not found'
    assert expected_message in message
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_product_when_objectives_doesnt_exists(api_client):
    product_data = ProductFactory.build()
    objective = ObjectiveFactory.create()
    pais = CountryFactory.create()
    category = CategoryFactory.create()
    data = {
        'pais': pais.nome,
        'nome': product_data.nome,
        'descricao': product_data.descricao,
        'conservacao': product_data.conservacao,
        'sugestao_de_uso': product_data.sugestao_de_uso,
        'categories': [category.nome],
        'objectives': ['Test'],
        'image_url': product_data.image_url,
        'modo_uso': product_data.modo_uso,
    }
    url = reverse('create_product')
    response = api_client.post(url, data=data, format='json')
    message = response.content.decode('utf-8')
    expected_message = "Objective Test not found"
    assert expected_message in message
    assert response.status_code == 400


@pytest.mark.django_db
def test_list_products(api_client):
    product_count = 5
    products = ProductFactory.create_batch(product_count)
    category = CategoryFactory.create()
    for product in products:
        product.categories.add(category)
    url = reverse('list_products')
    response = api_client.get(url)
    assert_valid_schema(response.data, 'catalogo_list_products.json')


@pytest.mark.django_db
def test_list_product(api_client):
    product = ProductFactory.create()
    category = CategoryFactory.create()
    url = reverse('list_product', args=[product.id])
    response = api_client.get(url)
    assert_valid_schema(response.data, 'catalogo_list_product.json')


@pytest.mark.django_db
def test_update_product_with_valid_data(api_client):
    category = CategoryFactory.create()
    pais = CountryFactory.create()
    objective = ObjectiveFactory.create()
    product_data = ProductFactory.create()
    product_before = Product.objects.get(id=product_data.id)
    new_country = CountryFactory.create()
    data = {
        'pais': new_country.nome,
        'nome': 'new nome',
        'descricao': product_data.descricao,
        'conservacao': product_data.conservacao,
        'sugestao_de_uso': product_data.sugestao_de_uso,
        'categories': [category.nome],
        'objectives': [objective.nome],
        'image_url': product_data.image_url,
        'modo_uso': product_data.modo_uso,
    }
    url = reverse('update_product', args=[product_data.id])
    response = api_client.put(url, data=data)
    product_after = Product.objects.get(id=product_data.id)
    _check_two_products_are_equal(product_after, data)


def _check_two_products_are_equal(product, data):
    product_categories_ids, data_categories_ids = _get_product_category_ids_and_data_categories_ids(
        data)

    assert product.nome == data['nome']
    assert product.pais.nome == data['pais']
    assert product.descricao == data['descricao']
    assert product.conservacao == data['conservacao']
    assert product.sugestao_de_uso == data['sugestao_de_uso']
    assert product.image_url == data['image_url']
    assert product.modo_uso == data['modo_uso']
    assert data_categories_ids == product_categories_ids


def _get_product_category_ids_and_data_categories_ids(data):
    product_categories_ids = list(Product.categories.through.objects.values_list(
        'category', flat=True).distinct().order_by('category_id'))
    data_category_ids = [Category.objects.get(
        nome=category).id for category in data['categories']]
    data_category_ids.sort()

    return product_categories_ids, data_category_ids
