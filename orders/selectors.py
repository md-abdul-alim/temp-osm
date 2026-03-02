from django.db.models import QuerySet
from .models import Order, Customer

def order_detail_selector(*, order_id: int) -> Order:
    return Order.objects.select_related('customer').prefetch_related('items__variant').get(id=order_id)

def customer_report_selector(*, customer_id: int) -> Customer:
    return Customer.objects.get(id=customer_id)
