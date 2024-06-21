from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django.shortcuts import redirect
from django.http import HttpResponseNotFound

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InventoryUpdateView(APIView):
    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_stock = request.data.get('stock', None)
        if new_stock is None or int(new_stock) <= 0:
            return Response({"error": "Invalid stock value"}, status=status.HTTP_400_BAD_REQUEST)
        
        product.stock += int(new_stock)
        product.save()
        return Response({"id": product.id, "sku": product.sku, "name": product.name, "stock": product.stock}, status=status.HTTP_200_OK)

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Vista personalizada para redirigir a /api/products
def redirect_to_products(request):
    return redirect('/api/products')

# Vista personalizada para manejar errores 404
def custom_page_not_found_view(request, exception=None):
    return redirect('/api/products')
