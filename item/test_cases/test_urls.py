from django.test import SimpleTestCase
from django.urls import resolve, reverse

from item import views


class TestItemUrls(SimpleTestCase):

    def test_new_url_resolves(self):
        url = reverse("item:new")
        self.assertEqual(resolve(url).func, views.new)

    def test_detail_url_resolves(self):
        url = reverse("item:detail", args=[1])
        self.assertEqual(resolve(url).func, views.detail)

    def test_delete_url_resolves(self):
        url = reverse("item:delete", args=[1])
        self.assertEqual(resolve(url).func, views.delete)

    def test_edit_url_resolves(self):
        url = reverse("item:edit", args=[1])
        self.assertEqual(resolve(url).func, views.edit)
