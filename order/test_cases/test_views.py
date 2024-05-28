import pytest
from django.urls import reverse
from django.contrib.auth.models import User

from cart.service import CartService
from order.models import Order, Address
from item.models import Item, Category


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category')


@pytest.fixture
def items(category, user):
    item1 = Item.objects.create(name='Item 1', category=category, created_by=user, price=10.0)
    item2 = Item.objects.create(name='Item 2', category=category, created_by=user, price=20.0)
    return [item1, item2]


@pytest.fixture
def address():
    return Address.objects.create(street='Test Street', city='Test City')


@pytest.fixture
def order(user, address):
    return Order.objects.create(user=user, address=address)


@pytest.mark.django_db
class TestOrderViews:
    def test_index_view(self, client, user):
        client.login(username='testuser', password='testpassword')
        url = reverse('order:index')
        response = client.get(url)
        assert response.status_code == 200

    def test_cancel_view(self, client, user, order):
        client.login(username='testuser', password='testpassword')
        url = reverse('order:cancel', args=[order.pk])
        response = client.get(url)
        assert response.status_code == 302  # Redirect to index
        assert not Order.objects.filter(pk=order.pk).exists()

    def test_detail_view(self, client, user, order):
        client.login(username='testuser', password='testpassword')
        url = reverse('order:detail', args=[order.pk])
        response = client.get(url)
        assert response.status_code == 200  # client’s request was successfully received

    @pytest.mark.django_db
    def test_checkout_view(self, client, user, items, address):
        client.login(username='testuser', password='testpassword')
        cart = CartService.get_or_create_cart(user)
        CartService.add_item_to_cart(cart, items[0], 2)
        CartService.add_item_to_cart(cart, items[1], 3)
        url = reverse('order:checkout')
        data = {
            'street': 'Test Street',
            'city': 'Test City',
            'zip_code': '12334',
            'state': 'kyiv',
            'house': 'some house'
        }
        response = client.post(reverse('order:checkout'), data=data)
        assert response.status_code == 302  # Redirect to payment

    def test_payment_view(self, client, user, order):
        client.login(username='testuser', password='testpassword')
        url = reverse('order:payment', args=[order.pk])
        response = client.get(url)
        assert response.status_code == 200  # client’s request was successfully received

        # Test paying for the order
        data = {
            'payment_method': 'credit_card',
            'card_number': '1234-5678-9012-3456',
            'expiry_date': '12/25',
            'cvv': '123',
        }
        response = client.post(url, data=data)
        assert response.status_code == 302  # Redirect to index
        order.refresh_from_db()
        assert order.paid
