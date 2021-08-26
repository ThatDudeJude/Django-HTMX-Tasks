from django.db import models
from django.conf import settings


# Create your models here.


class Task(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_priority = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        ordering = ["-updated"]
