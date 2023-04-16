from django.urls import path
from .views import *

urlpatterns = [
    path('create', ProductView.as_view(), name='create_product'),
    path('update/<int:product_id>', ProductView.as_view(), name='update_product'),
    path('list', ProductView.as_view(), name='list_products')
]