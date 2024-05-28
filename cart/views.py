from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cart.service import CartService
from item.models import Item


@login_required
def cart(request):
    current_user = request.user
    cart = CartService.get_or_create_cart(current_user)
    cart_items = cart.items.all()
    total = cart.get_total_cost()

    return render(request, 'cart/cart.html', {
        "cart_empty": len(cart_items) == 0,
        "cart_items": cart_items,
        "total": total
    })


@login_required
def cart_add(request, product_id):
    current_user = request.user
    item = get_object_or_404(Item, id=product_id)
    cart = CartService.get_or_create_cart(current_user)
    CartService.add_item_to_cart(cart, item, 1)
    return redirect('cart:cart')


@login_required
def cart_remove(request, product_id):
    current_user = request.user
    item = get_object_or_404(Item, id=product_id)
    cart = CartService.get_or_create_cart(current_user)
    CartService.remove_item_from_cart(cart, item, 1)
    return redirect('cart:cart')


@login_required
def cart_remove_completely(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    cart = CartService.get_or_create_cart(request.user)
    CartService.remove_item_from_cart_completely(cart, item)
    return redirect('cart:cart')

