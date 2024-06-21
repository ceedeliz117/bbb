from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'stock']
        read_only_fields = ['stock']

    def validate_sku(self, value):
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("SKU must be unique.")
        if len(value) < 5 or len(value) > 50:
            raise serializers.ValidationError("SKU must be between 5 and 50 characters.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value) < 3 or len(value) > 100:
            raise serializers.ValidationError("Name must be between 3 and 100 characters.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'ordered_at']

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        if data['quantity'] > data['product'].stock:
            raise serializers.ValidationError("Not enough stock available")
        return data

    def create(self, validated_data):
        product = validated_data['product']
        product.stock -= validated_data['quantity']
        product.save()
        return super().create(validated_data)
