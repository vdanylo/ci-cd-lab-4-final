from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from cart.service import CartService
from item.models import Item
from .forms import AddressForm, PaymentForm
from .models import Order, OrderItem
from .service import OrderService


@login_required()
def index(request):
    orders = request.user.orders.all()
    return render(request, 'order/index.html', {'orders': orders})


@login_required()
def cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    OrderService.cancel_order(order)
    return redirect('order:index')


@login_required()
def detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'order/detail.html', {'order': order})


@login_required()
def checkout(request):
    cart = CartService.get_or_create_cart(request.user)
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            try:
                address = address_form.save(commit=False)
                order = OrderService.create_order_from_cart(address, cart)
                return redirect('order:payment', order.id)

            except Exception as e:
                address_form.errors.append('error occured when making transaction, try again later.')
    else:
        address_form = AddressForm()

    items = cart.items.all()
    total_price = cart.get_total_cost()
    return render(request, "order/checkout.html", {
        'items': items,
        'address_form': address_form,
        'total_price': total_price})


@login_required()
def payment(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.paid:
        return HttpResponse("You have already paid!")

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            OrderService.pay_for_order(order)
            return redirect('index')
    else:
        payment_form = PaymentForm()

    return render(request, 'order/payment.html', context={'form': payment_form, 'order': order})
