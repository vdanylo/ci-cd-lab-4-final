from django.test import SimpleTestCase
from django.urls import resolve, reverse

from order import views

class TestOrderUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('order:index')
        self.assertEqual(resolve(url).func, views.index)

    def test_cancel_url_resolves(self):
        url = reverse('order:cancel', args=[1])
        self.assertEqual(resolve(url).func, views.cancel)

    def test_detail_url_resolves(self):
        url = reverse('order:detail', args=[1])
        self.assertEqual(resolve(url).func, views.detail)

    def test_checkout_url_resolves(self):
        url = reverse('order:checkout')
        self.assertEqual(resolve(url).func, views.checkout)

    def test_payment_url_resolves(self):
        url = reverse('order:payment', args=[1])
        self.assertEqual(resolve(url).func, views.payment)