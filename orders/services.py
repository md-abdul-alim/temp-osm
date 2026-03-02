from django.db import transaction
from .models import Order, OrderItem, Customer, Variant

def order_create(*, customer_id: int, items: list[dict]) -> Order:
    with transaction.atomic():
        customer = Customer.objects.select_for_update().get(id=customer_id)
        order = Order.objects.create(customer=customer)
        
        total_amount = 0
        order_items = []
        for item_data in items:
            variant = Variant.objects.get(id=item_data['variant_id'])
            order_item = OrderItem(
                order=order,
                variant=variant,
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            order_items.append(order_item)
            total_amount += item_data['price'] * item_data['quantity']
        
        for item in order_items:
            item.save()
        
        return order
