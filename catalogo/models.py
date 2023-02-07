from django.db import models

# Create your models here.
class Country(models.Model):
    nome = models.CharField(max_length=56)

class Product(models.Model):
    pais = models.ForeignKey(
        Country,
        on_delete=models.DO_NOTHING,
        blank=False,
        null = False,
    )
    nome = models.CharField(max_length=56)
    descricao = models.TextField()
    conservacao = models.TextField()
    sugestao_de_uso = models.TextField()
    image_url = models.CharField(max_length=255)
    modo_uso = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)