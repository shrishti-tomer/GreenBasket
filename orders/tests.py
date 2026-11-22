
from decimal import Decimal

from django.test import TestCase

from products.models import Category, Product

from .models import Order, OrderItem


class OrderModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Fruits",
            description="Fresh fruits"
        )

        self.product = Product.objects.create(
            name="Test Apples",
            description="Fresh apples",
            price=Decimal("2.50"),
            stock_quantity=20,
            category=self.category
        )

        self.order = Order.objects.create(
            customer_name="Test Customer",
            email="test@example.com",
            phone="0871234567",
            delivery_address="Newtownmountkennedy, Ireland",
            total_amount=Decimal("5.00")
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer_name, "Test Customer")
        self.assertEqual(self.order.email, "test@example.com")

    def test_order_default_status(self):
        self.assertEqual(self.order.status, "Pending")

    def test_order_item_subtotal(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal("2.50")
        )

        self.assertEqual(order_item.subtotal(), Decimal("5.00"))
