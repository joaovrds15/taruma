from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Product


class CreateProductView(generics.CreateAPIView):

    def post(self, request, *args,  **kwargs):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "product_id": serializer.data['id']
        }, status=status.HTTP_201_CREATED)
