import pytest
from django.contrib.auth.models import User
from item.models import Item, Category
from order.models import Order, Address, OrderItem
from order.service import OrderService

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser')

@pytest.fixture
def address():
    return Address.objects.create(street='Test Street', city='Test City')

@pytest.fixture
def category():
    return Category.objects.create(name='Test Category')

@pytest.fixture
def items(user, category):
    item1 = Item.objects.create(name='Item 1', category=category, created_by=user, price=10.0)
    item2 = Item.objects.create(name='Item 2', category=category, created_by=user, price=20.0)
    return [item1, item2]

@pytest.fixture
def order(user, address):
    return Order.objects.create(user=user, address=address)

@pytest.fixture
def order_with_items(order, items):
    for item in items:
        OrderItem.create_order_item_from_item(order, item).save()
    return order

@pytest.mark.django_db
class TestOrderService:
    def test_cancel_order(self, order):
        OrderService.cancel_order(order)
        assert not Order.objects.filter(pk=order.pk).exists()

    def test_create_order_from_items(self, user, address, items):
        order = OrderService.create_order_from_items(user, address, items)
        assert order.user == user
        assert order.address == address
        assert list(order.items.all()) == [
            OrderItem.create_order_item_from_item(order, item) for item in items
        ]

    def test_pay_for_order(self, order_with_items):
        order = order_with_items
        OrderService.pay_for_order(order)
        order.refresh_from_db()
        assert order.paid
        assert order.total_price == 30.0