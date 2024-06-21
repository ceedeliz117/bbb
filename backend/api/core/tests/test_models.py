import pytest
from core.models import Product, Order

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(sku='SKU_TEST', name='Test Product')
    assert product.sku == 'SKU_TEST'
    assert product.name == 'Test Product'
    assert product.stock == 100

@pytest.mark.django_db
def test_create_order():
    product = Product.objects.create(sku='SKU_TEST', name='Test Product')
    order = Order.objects.create(product=product, quantity=10)
    assert order.product == product
    assert order.quantity == 10
