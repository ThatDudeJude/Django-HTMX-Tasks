from django.test import TestCase
from django.urls import reverse
from .models import Task
from django.contrib.auth import get_user_model

# Create your tests here.


class TestTasks(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="pass12345"
        )
        cls.task1 = Task.objects.create(
            creator=cls.user,
            title="Test Task",
            body="This is a test task",
            is_priority=True,
        )

    def test_user_first_task(self):
        self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "pass12345"},
        )
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "tasks.html")
        self.assertContains(response, "Test Task")
        self.assertContains(response, "This is a test task")

        response = self.client.get(reverse("task", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "task.html")
        self.assertContains(response, "Test Task")
        self.assertContains(response, "This is a test task")

    def test_user_create_task(self):
        self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "pass12345"},
        )
        response = self.client.get(reverse("create"))
        self.assertTemplateUsed(response, "task_form.html")
        response = self.client.post(
            reverse("create"),
            {
                "title": "Second Test Task",
                "body": "This is the second test task",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task.html")
        self.assertContains(response, "Second Test Task")
        self.assertContains(response, "This is the second test task")

    def test_delete_task(self):
        self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "pass12345"},
        )
        response = self.client.get(reverse("create"))
        self.assertTemplateUsed(response, "task_form.html")
        response = self.client.post(
            reverse("create"),
            {
                "title": "Second Test Task",
                "body": "This is the second test task",
            },
            follow=True,
        )
        self.client.get("home")
        self.assertContains(response, "Second Test Task")
        response = self.client.post(reverse("delete", kwargs={"pk": 2}), follow=True)
        self.assertNotContains(response, "Second Test Task")
        self.assertContains(response, "This is a test task")
