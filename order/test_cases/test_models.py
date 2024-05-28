from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from order.models import Address, Order, OrderItem
from item.models import Item, Category
from order.service import OrderService


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def address():
    return Address.objects.create(
        house='123',
        street='Main St',
        city='Anytown',
        state='CA',
        zip_code='12345'
    )


@pytest.fixture
def category():
    return Category.objects.create(
        name="Some category 1"
    )


@pytest.fixture
def item(category, user):
    return Item.objects.create(name='Test Item', category=category, price=9.99, created_by=user)


@pytest.mark.django_db
def test_address_str_representation(address):
    assert str(address) == 'CA - Anytown - Main St - 123'


@pytest.mark.django_db
def test_order_str_representation(user):
    order = Order.objects.create(user=user)
    assert str(order).startswith('Order: ')


@pytest.mark.django_db
def test_order_total_price(user, address, item):
    order = Order.objects.create(user=user, address=address)
    order_item = OrderItem.create_order_item_from_item(order, item)
    order_item.save()
    expected_price = Decimal(str(item.price))
    assert order.get_current_total_price() == expected_price


@pytest.mark.django_db
def test_pay_for_order(user, address, item):
    order = Order.objects.create(user=user, address=address)
    OrderItem.create_order_item_from_item(order, item)
    OrderService.pay_for_order(order)
    assert order.paid is True
    assert order.total_price == order.get_current_total_price()


@pytest.mark.django_db
def test_order_item_str_representation(user, address, item):
    order = Order.objects.create(user=user, address=address)
    order_item = OrderItem.create_order_item_from_item(order, item)
    assert str(order_item).startswith('Order: ')


@pytest.mark.django_db
def test_order_item_get_cost(user, address, item):
    order = Order.objects.create(user=user, address=address)
    order_item = OrderItem.create_order_item_from_item(order, item)
    assert order_item.get_cost() == item.price


@pytest.mark.django_db
def test_create_order_item_from_item(user, address, item):
    order = Order.objects.create(user=user, address=address)
    order_item = OrderItem.create_order_item_from_item(order, item)
    assert order_item.order == order
    assert order_item.item == item
    assert order_item.quantity == 1
