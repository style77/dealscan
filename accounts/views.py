from typing import Any, Dict
from allauth.account.views import (
    SignupView,
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
)
from django.urls import reverse_lazy

from accounts.forms import CustomLoginForm, CustomResetPasswordForm, CustomSignupForm
from allauth.core import ratelimit


class MySignupView(SignupView):
    template_name = "signup.html"
    form_class = CustomSignupForm


class MyLoginView(LoginView):
    template_name = "login.html"
    form_class = CustomLoginForm


class MyPasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    form_class = CustomResetPasswordForm

    def get_success_url(self):
        return reverse_lazy("account_reset_password_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        r429 = ratelimit.consume_or_429(
            self.request,
            action="reset_password_email",
            key=email.lower(),
        )
        if r429:
            return r429
        form.save(self.request)

        self.request.session["reset_email"] = email

        return super(PasswordResetView, self).form_valid(form)


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"

    @staticmethod
    def _get_email_provider(email: str):
        if "@" in email:
            _, domain = email.split("@")
            return f"https://{domain}/"
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        email = self.request.session.get("reset_email")
        context["reset_email"] = email
        context["provider"] = self._get_email_provider(email)

        return context
