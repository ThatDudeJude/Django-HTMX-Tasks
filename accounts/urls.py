from django.urls import path
from .views import (
    CustomLogoutView,
    CustomProfileUpdateView,
    RegisterView,
    CustomLoginView,
    CustomProfileView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomConfirmPasswordReset,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", CustomProfileView.as_view(), name="profile"),
    path("profile/update/", CustomProfileUpdateView.as_view(), name="profile-update"),
    path(
        "password_change/", CustomPasswordChangeView.as_view(), name="password-change"
    ),
    path(
        "password_reset/", CustomPasswordResetView.as_view(), name="password-reset-form"
    ),
    path(
        "confirm_password_reset/<uidb64>/<token>/",
        CustomConfirmPasswordReset.as_view(),
        name="confirm-password-reset",
    ),
]
