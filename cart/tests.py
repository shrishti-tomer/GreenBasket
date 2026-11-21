
from decimal import Decimal
from django.test import TestCase
from products.models import Category, Product
from .models import CartItem


class CartItemModelTests(TestCase):

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

    def test_cart_item_creation(self):
        cart_item = CartItem.objects.create(
            product=self.product,
            session_key="test-session-123",
            quantity=2
        )

        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_item_subtotal(self):
        cart_item = CartItem.objects.create(
            product=self.product,
            session_key="test-session-123",
            quantity=3
        )

        self.assertEqual(cart_item.subtotal(), Decimal("7.50"))

    def test_cart_item_quantity(self):
        cart_item = CartItem.objects.create(
            product=self.product,
            session_key="test-session-123",
            quantity=5
        )

        self.assertEqual(cart_item.quantity, 5)
