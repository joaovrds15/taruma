from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Product
import json

class ProductView(APIView):
    def get(self, request, id = None):
        if id:
            product = Product.objects.get(id = id)
            serializer = ProductSerializer()
            data = serializer.format_response_list_one(product)
            return Response(data)

        products = Product.objects.all()
        serializer = ProductSerializer()
        data = serializer.format_response_list_all(products)
        return Response(data)

    def post(self, request, *args,  **kwargs):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "product_id": serializer.data['id']
        }, status=status.HTTP_201_CREATED)

    def put(self, request, product_id):
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)