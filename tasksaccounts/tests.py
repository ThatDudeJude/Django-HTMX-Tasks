from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from .models import TasksUser
from django.urls import reverse
import re

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

    def test_user_password_change(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.user.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("password-change"),
            {
                "old_password": self.user.password,
                "new_password1": "pass123456789",
                "new_password2": "pass123456789",
            },
        )
        self.client.get(reverse("logout"))
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": "pass123456789"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_password_reset(self):
        response = self.client.post(
            reverse("password-reset-form"), {"email": "test@email.com"}, follow=True
        )
        self.assertTemplateUsed(response, "registration/password_reset_done.html")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Reset your Tasks App account password"
        )

        mail_body = mail.outbox[0].body

        args = (
            re.search(
                "[\S\s]+(?<=/accounts/confirm_password_reset/)([\S]+)/", mail_body
            )
            .group(1)
            .split("/")
        )

        uid = args[0]
        token = args[1]

        response = self.client.get(
            "%s"
            % reverse("confirm-password-reset", kwargs={"uidb64": uid, "token": token}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_reset_confirm.html")
        response = self.client.post(
            "%s"
            % reverse("confirm-password-reset", kwargs={"uidb64": uid, "token": token}),
            {
                "new_password1": "pass12345678910",
                "new_password2": "pass12345678910",
            },
            follow=True,
        )

        self.assertTemplateUsed(response, "registration/password_reset_complete.html")

        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.user.password + "678910"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks.html")
        self.assertContains(response, "All Tasks")
