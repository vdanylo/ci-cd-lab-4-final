from django.db import models
from django.contrib.auth.models import User

from item.models import Item


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_total_cost(self):
        total_cost = 0
        for cart_item in self.items.all():
            total_cost += cart_item.item.price * cart_item.quantity
        return total_cost

    def __str__(self):
        return f"Cart #{self.pk} (User: {self.user.username})"

    def __iter__(self):
        for cart_item in self.items.all():
            yield cart_item


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
