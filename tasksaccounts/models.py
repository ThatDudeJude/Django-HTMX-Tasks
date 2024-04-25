import email
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER_CHOICES = (
    (None, "Choose your gender"),
    ("Male", "Male"),
    ("Female", "Female"),
    ("Custom", "Custom"),
    ("Prefer not to say", "Prefer not to say"),
)


class TasksUser(AbstractUser):
    name = models.CharField(blank=True, default="", max_length=30)
    email = models.EmailField(blank=False, null=False)
    occupation = models.CharField(blank=True, default="", max_length=30)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        TasksUser, related_name="profile", on_delete=models.CASCADE
    )
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=25)
    gender = models.CharField(
        choices=GENDER_CHOICES, null=True, blank=True, max_length=50
    )
    city = models.CharField(max_length=50, blank=True, null=True)
