from django.db import migrations, transaction

def create_initial_data(apps, schema_editor):
    Product = apps.get_model('core', 'Product')
    Inventory = apps.get_model('core', 'Inventory')
    Order = apps.get_model('core', 'Order')

    with transaction.atomic():
        product1 = Product.objects.create(sku='SKU001', name='Product 1')
        product2 = Product.objects.create(sku='SKU002', name='Product 2')
        product3 = Product.objects.create(sku='SKU003', name='Product 3')

        Inventory.objects.create(product=product1, quantity=50)
        Inventory.objects.create(product=product2, quantity=75)
        Inventory.objects.create(product=product3, quantity=100)

        Order.objects.create(product=product1, quantity=5)
        Order.objects.create(product=product2, quantity=10)
        Order.objects.create(product=product3, quantity=15)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
