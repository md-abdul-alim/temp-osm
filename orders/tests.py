from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Customer, Variant, Order, OrderItem

class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Test Customer", email="test@example.com")
        self.variant = Variant.objects.create(name="Test Variant", cost_price=50.00, selling_price=100.00)
        self.create_url = reverse('order-create')

    def test_order_create_success(self):
        data = {
            "customer_id": self.customer.id,
            "items": [
                {
                    "variant_id": self.variant.id,
                    "quantity": 2,
                    "price": 100.00
                }
            ]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify customer total spent
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_spent, 200.00)
        
        # Verify order exists
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_order_create_price_below_cost_fails(self):
        data = {
            "customer_id": self.customer.id,
            "items": [
                {
                    "variant_id": self.variant.id,
                    "quantity": 1,
                    "price": 40.00  # Below cost price 50.00
                }
            ]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Price cannot be below variant cost price", str(response.data))

    def test_order_create_invalid_customer_fails(self):
        data = {
            "customer_id": 9999,
            "items": [
                {
                    "variant_id": self.variant.id,
                    "quantity": 1,
                    "price": 100.00
                }
            ]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_create_invalid_variant_fails(self):
        data = {
            "customer_id": self.customer.id,
            "items": [
                {
                    "variant_id": 9999,
                    "quantity": 1,
                    "price": 100.00
                }
            ]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_item_delete_updates_total_spent(self):
        # Create an order and item
        order = Order.objects.create(customer=self.customer)
        item = OrderItem.objects.create(order=order, variant=self.variant, quantity=1, price=Decimal('100.00'))
        
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_spent, Decimal('100.00'))
        
        # Delete the item
        item.delete()
        
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_spent, Decimal('0.00'))
