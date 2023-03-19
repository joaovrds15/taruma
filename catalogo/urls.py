from django.urls import path
from .views import *

urlpatterns = [
    path('create',CreateProductView.as_view(), name='create_product'),
]