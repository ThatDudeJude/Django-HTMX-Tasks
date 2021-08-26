from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import Profile, TasksUser
from django.views import View
from .forms import MyUserCreationForm, MyUserProfileForm


# Create your views here.
class CustomLoginView(LoginView):
    # redirect_authenticated_user = True
    main_base_template = "main.html"
    base_base_template = "base.html"
    redirect_authenticated_user = True
    next_page = "/"

    def get(self, request, *args, **kwargs):
        if request.htmx:
            base_template = self.main_base_template
        else:
            base_template = self.base_base_template
        form = self.form_class()
        context = self.get_context_data()
        context["form"] = form
        context["base_template"] = base_template
        return render(
            request,
            "registration/login.html",
            context,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = "/"
        context["base_template"] = self.main_base_template
        return context

    # def post(self, request, *args, **kwargs):
    #     print("Signing in")
    #     context = self.get_context_data()
    #     print(context)
    #     return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(form.is_valid(), request.POST)
        if not form.is_valid():
            print("Form is not valid")
            context = self.get_context_data()
            context["form"] = form
            context["base_template"] = self.base_base_template
            return render(
                request,
                "registration/login.html",
                context,
            )

        else:

            return self.form_valid(form)


class RegisterView(View):
    main_base_template = "main.html"
    base_base_template = "base.html"
    form_class = MyUserCreationForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        if request.htmx:
            base_template = self.main_base_template
        else:
            base_template = self.base_base_template

        return render(
            request,
            "registration/signup.html",
            {"base_template": base_template, "form": form},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            context = {"form": form, "base_template": self.base_base_template}
            return render(
                request,
                "registration/signup.html",
                context,
            )


class CustomLogoutView(LogoutView):
    next_page = "login"


@method_decorator(login_required, name="dispatch")
class CustomProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, _ = Profile.objects.get_or_create(user=request.user)
        return super(CustomProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"
        print("User", self.profile.user.email)
        return render(
            request,
            "registration/profile.html",
            {
                "base_template": base_template,
                "profile": self.profile,
            },
        )


@method_decorator(login_required, name="dispatch")
class CustomProfileUpdateView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, _ = Profile.objects.get_or_create(user=request.user)
        return super(CustomProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"

        profile_form = MyUserProfileForm(
            instance=self.profile,
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            },
        )
        print("User", self.profile.user.email)
        print(request.user)
        print("profile", profile_form.Meta.fields)
        return render(
            request,
            "registration/profile_form.html",
            {
                "base_template": base_template,
                "profile_form": profile_form,
            },
        )

    def post(self, request):

        profile_form = MyUserProfileForm(request.POST, instance=self.profile)

        if profile_form.is_valid():
            profile = profile_form.save()
            profile.user.first_name = profile_form.cleaned_data.get("first_name")
            profile.user.last_name = profile_form.cleaned_data.get("last_name")
            profile.user.email = profile_form.cleaned_data.get("email")
            profile.user.save()
            return redirect("profile")
        else:
            return render(
                request,
                "registration/profile_form.html",
                {
                    "base_template": "main.html",
                    "profile_form": profile_form,
                },
            )


@method_decorator(login_required, name="dispatch")
class CustomPasswordChangeView(View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"
        context = {
            "base_template": base_template,
            "form": form,
        }

        return render(request, "registration/password_change_form.html", context)

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            context = {"base_template": "main.html"}
            update_session_auth_hash(request, form.user)
            return render(request, "registration/password_change_done.html", context)

        context = {"base_template": "main.html", "form": form}
        return render(request, "registration/password_change_form.html", context)


token_generator = PasswordResetTokenGenerator()


class CustomPasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"
        context = {
            "base_template": base_template,
            "form": form,
        }

        return render(request, "registration/password_reset_form.html", context)

    def post(self, request):
        form = PasswordResetForm(request.POST)
        email = request.POST.get("email")
        if form.is_valid():
            try:
                TasksUser.objects.get(email=email)
            except TasksUser.DoesNotExist:
                context = {
                    "base_template": "main.html",
                    "form": form,
                    "message": "The email address you entered is not registered with an account.",
                }
                return render(request, "registration/password_reset_form.html", context)
            else:
                tasksuser = TasksUser.objects.get(email=email)
                protocol = "https" if request.is_secure() else "http"
                opts = {
                    "use_https": request.is_secure(),
                    "request": request,
                    "from_email": "gachjude@gmail.com",
                    "subject_template_name": "registration/password_reset_subject.txt",
                    "email_template_name": "registration/password_reset_email.html",
                    "extra_email_context": {
                        "site_name": "Tasks App",
                        "domain": request.get_host(),
                        "protocol": protocol,
                        "uid": urlsafe_base64_encode(force_bytes(tasksuser.pk)),
                        "token": token_generator.make_token(tasksuser),
                    },
                }
                form.save(**opts)
                return render(
                    request,
                    "registration/password_reset_done.html",
                    {"base_template": "main.html"},
                )


class CustomConfirmPasswordReset(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = TasksUser.objects.get(pk=uid)
        except (TasksUser.DoesNotExist, TypeError, ValueError, OverflowError):
            user = None

        else:
            if token_generator.check_token(user, token) and user is not None:
                form = SetPasswordForm(user=user)

                context = {"form": form, "base_template": "base.html"}

                return render(
                    request, "registration/password_reset_confirm.html", context
                )

        context = {"message": "Bad request!", "base_template": "base.html"}
        return render(request, "error.html", context)

    def post(self, request, uidb64):
        uid = urlsafe_base64_decode(uidb64)
        user = TasksUser.objects.get(pk=uid)
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            logout(request)
            context = {"base_template": "main.html"}
            return render(request, "registration/password_change_done.html", context)
        else:
            context = {"form": form, "base_template": "main.html"}

            return render(request, "registration/password_reset_confirm.html", context)
