from rest_framework import serializers
from .models import Customer, Variant, Order, OrderItem

class OrderItemCreateSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        try:
            variant = Variant.objects.get(id=data['variant_id'])
        except Variant.DoesNotExist:
            raise serializers.ValidationError({"variant_id": "Variant does not exist."})
        
        if data['price'] < variant.cost_price:
            raise serializers.ValidationError({"price": f"Price cannot be below variant cost price ({variant.cost_price})."})
        
        return data

class OrderCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    items = OrderItemCreateSerializer(many=True)

    def validate_customer_id(self, value):
        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Customer does not exist.")
        return value

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        return value

class OrderItemDetailSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source='variant.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'variant_id', 'variant_name', 'quantity', 'price']

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(source='total_price', max_digits=10, decimal_places=2)
    customer_name = serializers.CharField(source='customer.name')

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'customer_name', 'items', 'total_amount', 'created_at']

class CustomerReportSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(source='id')
    customer_name = serializers.CharField(source='name')
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)
