from django.db import models

class Category(models.Model):
    nome = models.CharField(max_length=56)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome}"

class Country(models.Model):
    nome = models.CharField(max_length=56, unique=True)

    def __str__(self):
        return self.nome

class Objective(models.Model):
    nome = models.CharField(max_length=56)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    categories = models.ManyToManyField(Category)
    objectives = models.ManyToManyField(Objective)
    image_url = models.CharField(max_length=255, null=True)
    modo_uso = models.TextField()
    show_product = models.BooleanField(default = True, null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.pais.nome}): {self.descricao} {self.categories}"
    
class Lote(models.Model):
    produto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=False,
        null = False,
    )
    numero = models.IntegerField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    unidade_medida = models.CharField(max_length=3)
    data_fabricacao = models.DateField()
    data_vencimento = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)