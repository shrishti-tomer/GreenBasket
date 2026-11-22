
from django.core.management.base import BaseCommand

from products.models import Category, Product


class Command(BaseCommand):
    help = "Add 20 sample fruits and vegetables to GreenBasket"

    def handle(self, *args, **kwargs):

        fruits, _ = Category.objects.get_or_create(
            name="Fruits",
            defaults={"description": "Fresh and seasonal fruits"}
        )

        vegetables, _ = Category.objects.get_or_create(
            name="Vegetables",
            defaults={"description": "Fresh and seasonal vegetables"}
        )

        products = [
            # Fruits
            ("Organic Apples", "Fresh and naturally grown organic apples.", 2.50, 50, fruits),
            ("Bananas", "Fresh ripe bananas.", 1.50, 60, fruits),
            ("Oranges", "Juicy and fresh oranges.", 2.00, 45, fruits),
            ("Mangoes", "Sweet and delicious mangoes.", 3.00, 30, fruits),
            ("Grapes", "Fresh seedless grapes.", 2.75, 35, fruits),
            ("Strawberries", "Fresh and sweet strawberries.", 3.50, 25, fruits),
            ("Pineapples", "Fresh tropical pineapples.", 3.00, 20, fruits),
            ("Watermelons", "Refreshing and juicy watermelons.", 4.00, 15, fruits),
            ("Papayas", "Fresh and ripe papayas.", 2.80, 20, fruits),
            ("Pears", "Sweet and fresh pears.", 2.25, 30, fruits),

            # Vegetables
            ("Carrots", "Fresh and crunchy carrots.", 1.20, 50, vegetables),
            ("Tomatoes", "Fresh red tomatoes.", 2.00, 45, vegetables),
            ("Potatoes", "Fresh everyday potatoes.", 1.50, 70, vegetables),
            ("Onions", "Fresh cooking onions.", 1.30, 60, vegetables),
            ("Broccoli", "Fresh green broccoli.", 2.50, 30, vegetables),
            ("Spinach", "Fresh leafy spinach.", 1.80, 25, vegetables),
            ("Cucumbers", "Fresh and crunchy cucumbers.", 1.40, 35, vegetables),
            ("Bell Peppers", "Colourful fresh bell peppers.", 2.20, 30, vegetables),
            ("Cauliflower", "Fresh white cauliflower.", 2.00, 25, vegetables),
            ("Cabbage", "Fresh green cabbage.", 1.60, 30, vegetables),
        ]

        for name, description, price, stock, category in products:
            Product.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": price,
                    "stock_quantity": stock,
                    "category": category,
                }
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully added or updated 20 sample products!")
        )
