from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import OrderItem, Customer

@receiver(post_save, sender=OrderItem)
def update_customer_total_spent_on_save(sender, instance, created, **kwargs):
    if created:
        customer = instance.order.customer
        customer.total_spent += instance.price * instance.quantity
        customer.save(update_fields=['total_spent'])

@receiver(pre_delete, sender=OrderItem)
def update_customer_total_spent_on_delete(sender, instance, **kwargs):
    customer = instance.order.customer
    customer.total_spent -= instance.price * instance.quantity
    customer.save(update_fields=['total_spent'])
