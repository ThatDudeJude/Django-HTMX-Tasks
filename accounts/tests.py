from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TasksUser
from django.urls import reverse

# Create your tests here.


class TasksUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="testuser", email="test@email.com", password="pass12345"
        )

    def test_created_test_user(self):
        user = get_user_model().objects.all().first()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.password, "pass12345")
        self.assertEqual(get_user_model().objects.count(), 1)


class TestAuthentication(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username="testuser", email="test@email.com", password="pass12345"
        )

    def test_user_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuserregister",
                "email": "testregister@email.com",
                "password1": "pass54321",
                "password2": "pass54321",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all()[1].username, "testuserregister")
        self.assertEqual(
            get_user_model().objects.all()[1].email, "testregister@email.com"
        )

    def test_user_login(self):
        user = get_user_model().objects.create_user(
            username="testuser2", email="test2@email.com", password="pasw12345"
        )
        user.save()
        response = self.client.post(
            "/accounts/login/",
            {
                "username": "testuser2",
                "password": "pasw12345",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks.html")
        self.assertContains(response, "All Tasks")
