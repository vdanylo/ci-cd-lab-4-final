from decimal import Decimal
from typing import List

from django.db import models, transaction
from django.contrib.auth.models import User

from cart.models import CartItem
from item.models import Item
from django.core.validators import MinValueValidator


class Address(models.Model):
    house = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.state} - {self.city} - {self.street} - {self.house}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order: {self.id} - By: {self.user.username} - Date: [{self.created_at}]"

    def get_current_total_price(self) -> Decimal:
        """
        Returns sum of all prices of ordered items.
        """
        total = sum(item.get_cost() for item in self.items.all())
        total = Decimal(total)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Order: {self.order.id} - Item: {self.item.name}"

    def __eq__(self, other):
        if not isinstance(other, OrderItem):
            return False
        return (
                self.order == other.order
                and self.item == other.item
                and self.quantity == other.quantity
        )

    def get_cost(self) -> Decimal:
        """
        Returns item price multiplied by quantity.
        """
        return Decimal(self.item.price * self.quantity)

    @staticmethod
    def create_order_item_from_item(order: Order, item: Item):
        """
        Creates and returns order item based on item, with quantity = 1.
        """
        order_item = OrderItem(
            order=order,
            item=item,
            quantity=1
        )
        return order_item

    @staticmethod
    def create_order_item_from_cart_item(order: Order, cart_item: CartItem):
        """
        Creates and returns order item based on item, with quantity = 1.
        """
        order_item = OrderItem(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity
        )
        return order_item
