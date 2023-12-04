from typing import Any, Dict

from allauth.account import app_settings, signals
from allauth.account.adapter import get_adapter
from allauth.account.decorators import reauthentication_required
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation, sync_user_email_addresses
from allauth.account.views import (
    AjaxCapableProcessFormViewMixin,
    ConfirmEmailView,
    EmailVerificationSentView,
    LoginView,
    PasswordResetDoneView,
    PasswordResetView,
    SignupView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    _ajax_response,
)
from allauth.core import ratelimit
from allauth.decorators import rate_limit
from django.contrib import messages
from django.core.validators import validate_email
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from accounts.forms import (
    AccountForm,
    CustomLoginForm,
    CustomResetPasswordForm,
    CustomSignupForm,
    CustomResetPasswordKeyForm,
)


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


class MyConfirmEmailView(ConfirmEmailView):
    template_name = "email_confirm.html"


class VerificationEmailSent(EmailVerificationSentView):
    template_name = "verification_sent.html"


@method_decorator(rate_limit(action="manage_email"), name="dispatch")
@method_decorator(
    reauthentication_required(
        allow_get=True, enabled=lambda request: app_settings.REAUTHENTICATION_REQUIRED
    ),
    name="dispatch",
)
class MyEmailView(AjaxCapableProcessFormViewMixin, FormView):
    template_name = "management.html"
    form_class = AccountForm
    success_url = reverse_lazy("account")

    def get_form_class(self) -> type:
        return self.form_class

    def dispatch(self, request, *args, **kwargs):
        sync_user_email_addresses(request.user)
        return super(MyEmailView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(MyEmailView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self) -> Dict[str, Any]:
        user = self.request.user
        initial = {
            "username": user.username,
            "email": EmailAddress.objects.get_verified(user),
            "phone": user.phone_number,
        }
        self.initial.update(initial)

        return super().get_initial()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update(
            {
                "new_emailaddress": EmailAddress.objects.get_new(user),
                "current_emailaddress": EmailAddress.objects.get_verified(user),
            }
        )

        return context

    def form_valid(self, form):
        changes = form.save(self.request)

        if changes and changes.email_changed:
            get_adapter(self.request).add_message(
                self.request,
                messages.INFO,
                "account/messages/email_confirmation_sent.html",
                {"email": form.cleaned_data["email"]},
            )
            signals.email_added.send(
                sender=self.request.user.__class__,
                request=self.request,
                user=self.request.user,
                email_address=changes.email_address,
            )
        return super(MyEmailView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        res = None
        if request.POST.get("email") and "action_send" in request.POST:
            res = self._resend_verification(request)
        elif "action_edit" in request.POST:
            form = self.get_form()
            if form.is_valid():  # TODO WHY IS FORM NOT CALLED BY ITSELF?
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            res = HttpResponseRedirect(self.success_url)
            return _ajax_response(request, res, data=self._get_ajax_data_if())

        res = res or HttpResponseRedirect(self.get_success_url())
        res = _ajax_response(request, res, data=self._get_ajax_data_if())
        return res

    def _get_email_address(self, request):
        email = request.POST["email"]
        try:
            validate_email(email)
        except ValidationError:
            return None
        try:
            return EmailAddress.objects.get_for_user(user=request.user, email=email)
        except EmailAddress.DoesNotExist:
            pass

    def _resend_verification(self, request, *args, **kwargs):
        email_address = self._get_email_address(request)
        if email_address:
            send_email_confirmation(
                self.request, request.user, email=email_address.email
            )


class MyPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = "password_reset_from_key.html"
    form_class = CustomResetPasswordKeyForm

    def form_valid(self, form):
        print("valid")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class MyPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = "password_reset_from_key_done.html"
