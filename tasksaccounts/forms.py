from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
)
from django import forms
from .models import TasksUser, Profile


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = TasksUser
        fields = UserCreationForm.Meta.fields + ("name", "email", "occupation")


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = TasksUser
        fields = UserChangeForm.Meta.fields


class MyUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "gender",
            "phone",
            "city",
            "birthday",
            "email",
        ]
        exclude = ["user"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "birthday": forms.TextInput(attrs={"type": "date"}),
        }
