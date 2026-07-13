from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


class HomeViewTest(TestCase):

    def setUp(self):
        cache.clear()

        User.objects.create_user(username="rakib", password="123456")
        User.objects.create_user(username="hasan", password="123456")

    def test_home_page_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_contains_title(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Welcome to the Django Docker CI/CD Project!")

    def test_users_are_cached(self):
        self.client.get(reverse("home"))
        users = cache.get("users")
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 2)