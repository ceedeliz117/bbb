from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=100)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order of {self.quantity} {self.product.name}"
