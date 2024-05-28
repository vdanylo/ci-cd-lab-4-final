from django.contrib.auth.models import User
from django.db import transaction
from cart.models import Cart, CartItem
from item.models import Item


class CartService:

    @staticmethod
    @transaction.atomic
    def get_or_create_cart(user: User) -> Cart:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    @transaction.atomic
    def add_item_to_cart(cart: Cart, item: Item, quantity: int) -> CartItem:
        quantity = abs(quantity)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            item=item,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity

        cart_item.save()

        return cart_item

    @staticmethod
    @transaction.atomic
    def remove_item_from_cart(cart: Cart, item: Item, quantity: int) -> None:
        try:
            quantity = abs(quantity)
            cart_item = CartItem.objects.filter(cart=cart, item=item).first()
            cart_item.quantity -= quantity

            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        except CartItem.DoesNotExist:
            pass


    @staticmethod
    @transaction.atomic
    def remove_item_from_cart_completely(cart: Cart, item: Item) -> None:
        try:
            cart_item = CartItem.objects.get(cart=cart, item=item)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass