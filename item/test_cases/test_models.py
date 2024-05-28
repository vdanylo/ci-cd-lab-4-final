from django.contrib.auth.models import User
from django.test import TestCase

from item.models import Category, Item


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test category
        Category.objects.create(name="Test Category", description="A test category")

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field("description").verbose_name
        self.assertEquals(field_label, "description")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")

    def test_object_name_is_name_field(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEquals(expected_object_name, str(category))


class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        test_user = User.objects.create_user(username="testuser", password="12345")

        # Create a test category
        test_category = Category.objects.create(name="Test Category")

        # Create a test item
        Item.objects.create(
            name="Test Item",
            description="A test item",
            price=10,
            category=test_category,
            created_by=test_user,
        )

    def test_name_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_description_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("description").verbose_name
        self.assertEquals(field_label, "description")

    def test_price_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("price").verbose_name
        self.assertEquals(field_label, "price")

    def test_category_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("category").verbose_name
        self.assertEquals(field_label, "category")

    def test_image_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("image").verbose_name
        self.assertEquals(field_label, "image")

    def test_created_at_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("created_at").verbose_name
        self.assertEquals(field_label, "created at")

    def test_is_sold_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("is_sold").verbose_name
        self.assertEquals(field_label, "is sold")

    def test_created_by_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field("created_by").verbose_name
        self.assertEquals(field_label, "created by")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Item._meta.verbose_name_plural), "items")

    def test_object_name_is_name_field(self):
        item = Item.objects.get(id=1)
        expected_object_name = item.name
        self.assertEquals(expected_object_name, str(item))
