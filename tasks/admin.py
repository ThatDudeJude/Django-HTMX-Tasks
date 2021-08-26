from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Task

# Register your models here.


class TaskAdmin(ModelAdmin):
    list_display = ["id", "title", "is_priority"]


admin.site.register(Task, TaskAdmin)
