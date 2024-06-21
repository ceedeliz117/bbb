import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Product, Order

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_product():
    def _create_product(sku, name, stock=100):
        return Product.objects.create(sku=sku, name=name, stock=stock)
    return _create_product

# Test para Crear Producto
@pytest.mark.django_db(transaction=True)
def test_create_product(api_client):
    response = api_client.post(reverse('product-list-create'), {'sku': 'SKU12345', 'name': 'Test Product'})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['sku'] == 'SKU12345'
    assert response.json()['name'] == 'Test Product'
    assert response.json()['stock'] == 100

@pytest.mark.django_db(transaction=True)
def test_create_product_invalid_data(api_client):
    response = api_client.post(reverse('product-list-create'), {'sku': 'SKU', 'name': ''})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'sku' in response.json()
    assert 'name' in response.json()

# Test para Actualizar Inventario
@pytest.mark.django_db(transaction=True)
def test_update_inventory(api_client, create_product):
    product = create_product(sku='SKU12345', name='Test Product', stock=100)
    response = api_client.patch(reverse('inventory-update', args=[product.id]), {'stock': 50})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['stock'] == 150

@pytest.mark.django_db(transaction=True)
def test_update_inventory_invalid_data(api_client, create_product):
    product = create_product(sku='SKU12345', name='Test Product', stock=100)
    response = api_client.patch(reverse('inventory-update', args=[product.id]), {'stock': -10})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.json()

# Test para Crear Pedido
@pytest.mark.django_db(transaction=True)
def test_create_order(api_client, create_product):
    product = create_product(sku='SKU12345', name='Test Product', stock=100)
    response = api_client.post(reverse('order-create'), {'product': product.id, 'quantity': 10})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['product'] == product.id
    assert response.json()['quantity'] == 10
    updated_product = Product.objects.get(id=product.id)
    assert updated_product.stock == 90

@pytest.mark.django_db(transaction=True)
def test_create_order_insufficient_stock(api_client, create_product):
    product = create_product(sku='SKU12345', name='Test Product', stock=5)
    response = api_client.post(reverse('order-create'), {'product': product.id, 'quantity': 10})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.json()
    assert response.json()['non_field_errors'] == ['Not enough stock available']

# Test para Obtener Detalles del Producto
@pytest.mark.django_db(transaction=True)
def test_get_product_detail(api_client, create_product):
    product = create_product(sku='SKU12345', name='Test Product')
    response = api_client.get(reverse('product-detail', args=[product.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['sku'] == 'SKU12345'
    assert response.json()['name'] == 'Test Product'
    assert response.json()['stock'] == 100

# Test para Verificar la Reducción del Stock al Hacer una Orden
@pytest.mark.django_db(transaction=True)
def test_order_reduces_stock(api_client, create_product):
    product = create_product(sku='SKU67890', name='Another Test Product', stock=50)
    
    # Crear una orden de 20 unidades del producto
    response = api_client.post(reverse('order-create'), {'product': product.id, 'quantity': 20})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['product'] == product.id
    assert response.json()['quantity'] == 20

    # Verificar que el stock del producto se ha reducido correctamente
    updated_product = Product.objects.get(id=product.id)
    assert updated_product.stock == 30
