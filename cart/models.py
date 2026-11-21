
from django.db import models
from products.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    session_key = models.CharField(max_length=40)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
