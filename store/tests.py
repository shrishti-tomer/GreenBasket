
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product


class StoreViewTests(TestCase):

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

    def test_store_page_loads(self):
        response = self.client.get(reverse("store_home"))

        self.assertEqual(response.status_code, 200)

    def test_store_page_displays_products(self):
        response = self.client.get(reverse("store_home"))

        self.assertContains(response, "Test Apples")

    def test_store_page_displays_categories(self):
        response = self.client.get(reverse("store_home"))

        self.assertContains(response, "Fruits")
