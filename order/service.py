from typing import List
from django.contrib.auth.models import User
from django.db import transaction

from cart.models import Cart
from item.models import Item
from order.models import Order, Address, OrderItem


class OrderService:

    @staticmethod
    def cancel_order(order: Order):
        """
        Well, it just deletes order.
        """
        order.delete()

    @staticmethod
    def create_order_from_items(user: User, address: Address, cart: List[Item]) -> Order:
        """
        Starts transaction that creates order and
        order items in db, based on user, delivery address and
        list of items. Returns created order.
        """
        with transaction.atomic():
            address.save()
            order = Order.objects.create(user=user, address=address)
            for item in cart:
                order_item = OrderItem.create_order_item_from_item(order, item)
                order_item.save()
            order.save()
            return order

    @staticmethod
    def create_order_from_cart(address: Address, cart: Cart) -> Order:
        """
        Starts transaction that creates order and
        order items in db, based on cart and address and.
        Deletes cart after transaction, returns created order.
        """
        with transaction.atomic():
            if len(cart.items.all()) == 0:
                raise Exception("Your cart is empty")

            address.save()
            order = Order.objects.create(user=cart.user, address=address)
            for cart_item in cart:
                order_item = OrderItem.create_order_item_from_cart_item(order, cart_item)
                order_item.save()
            cart.delete()
            order.save()
            return order

    @staticmethod
    def pay_for_order(order) -> None:
        """
        Starts transaction. Makes order paid status = True and saves
        total price on paying moment
        """
        with transaction.atomic():
            order.total_price = order.get_current_total_price()
            order.paid = True
            order.save()
