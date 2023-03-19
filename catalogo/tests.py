from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *

# Create your tests here.
class CreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('create')
        """ self.product = Product.objects.create(
            nome = 'Castanha',
            descricao = 'Lorem ipsum dolor sit ammet',
            conservacao = 'Colocar na geladeira',
            sugestao_de_uso = 'Comer com farinha',
            categories = [
                Category.objects.create(nome = 'teste')
            ]
        ) """

        def test_create_with_valid_product_info(self):
            data = {
                'nome' : 'Castanha',
                'descricao' : 'Lorem ipsum dolor sit ammet',
                'conservacao' : 'Colocar na geladeira',
                'sugestao_de_uso' : 'Comer com farinha',
            }
            response = self.client.post(self.url, data, format='json')
            raise Exception('chamou')
            
            