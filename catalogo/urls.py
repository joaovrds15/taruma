from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catalogo import views

urlpatterns = [
    path('create', views.create.as_view()),
    path('create/lote', views.create.as_view()),
]