from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TasksUser
from tasks.models import Task
from .forms import MyUserCreationForm, MyUserChangeForm

# Register your models here.


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class TasksUserModelAdmin(UserAdmin):

    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = TasksUser
    list_display = ["id", "email", "occupation", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "name",
                    # "email",
                    "occupation",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "name",
                    # "email",
                    "occupation",
                )
            },
        ),
    )
    inlines = [TaskInline]


admin.site.register(TasksUser, TasksUserModelAdmin)
