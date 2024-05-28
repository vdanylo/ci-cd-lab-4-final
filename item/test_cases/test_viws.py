from io import BytesIO

from django.contrib.auth.models import User
from django.db.models.fields.files import File
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

from item.models import Category, Item


class ItemDetailViewTest(TestCase):
    @staticmethod
    def get_image_file(name, ext="png", size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()

        # Создаем категории и товары для тестов
        self.category = Category.objects.create(name="TestCategory")

        # Создаем тестовое изображение
        image = self.get_image_file("image.png")

        self.item = Item.objects.create(
            name="Test Item",
            category=self.category,
            description="A test item",
            price=10,
            is_sold=False,
            created_by=self.user,
            image=image,
        )

    def test_detail_view_context(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("item:detail", kwargs={"pk": self.item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("item", response.context)
        self.assertIn("related_items", response.context)
        self.assertEqual(response.context["item"], self.item)
        self.assertQuerysetEqual(
            response.context["related_items"],
            Item.objects.filter(category=self.item.category, is_sold=False).exclude(
                pk=self.item.pk
            ),
            transform=lambda x: x,
        )

    def test_new_item_view(self):
        self.client.login(username="testuser", password="12345")

        image_file = self.get_image_file("test_image.jpg")

        response = self.client.get(reverse("item:new"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("item:new"),
            {
                "name": "New Test Item",
                "category": self.category.id,
                "description": "A new test item",
                "price": 20,
                "image": image_file,
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_item_view(self):
        # Входим в систему
        self.client.login(username="testuser", password="12345")

        # Создаем временный файл изображения для загрузки
        image_file = self.get_image_file("test_image.jpg")

        # Редактируем товар
        response = self.client.post(
            reverse("item:edit", kwargs={"pk": self.item.pk}),
            {
                "name": "Edited Test Item",
                "category": self.category.id,
                "description": "An edited test item",
                "price": 30,
                "image": image_file,
            },
        )

        # Проверяем, что после успешного редактирования объекта происходит редирект на страницу деталей
        self.assertEqual(response.status_code, 302)

        # Проверяем, что объект был действительно отредактирован
        edited_item = Item.objects.get(pk=self.item.pk)
        self.assertEqual(edited_item.name, "Edited Test Item")
        self.assertEqual(edited_item.description, "An edited test item")
        self.assertEqual(edited_item.price, 30)

    def test_delete_item_view(self):
        # Входим в систему
        self.client.login(username="testuser", password="12345")

        # Удаляем товар
        response = self.client.post(reverse("item:delete", kwargs={"pk": self.item.pk}))

        # Проверяем, что после успешного удаления объекта происходит редирект на главную страницу
        self.assertEqual(response.status_code, 302)

        # Проверяем, что объект был действительно удален
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=self.item.pk)
