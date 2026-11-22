
from decimal import Decimal

from django.test import TestCase

from .models import Category, Product


class ProductModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Fruits",
            description="Fresh and seasonal fruits"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Fruits")
        self.assertEqual(str(self.category), "Fruits")

    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Apples",
            description="Fresh apples",
            price=Decimal("2.50"),
            stock_quantity=20,
            category=self.category
        )

        self.assertEqual(product.name, "Test Apples")
        self.assertEqual(product.price, Decimal("2.50"))
        self.assertEqual(product.category, self.category)

    def test_product_stock_quantity(self):
        product = Product.objects.create(
            name="Test Bananas",
            description="Fresh bananas",
            price=Decimal("1.50"),
            stock_quantity=15,
            category=self.category
        )

        self.assertEqual(product.stock_quantity, 15)
