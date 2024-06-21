from django.urls import path
from .views import ProductListCreateView, ProductDetailView, InventoryUpdateView, OrderCreateView

urlpatterns = [
    path('products', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('inventories/product/<int:pk>', InventoryUpdateView.as_view(), name='inventory-update'),
    path('orders', OrderCreateView.as_view(), name='order-create'),
]
