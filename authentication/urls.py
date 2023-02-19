from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework.permissions import IsAuthenticated

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(),name='login'),
]