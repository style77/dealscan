from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import AddEmailForm
from allauth.account.models import EmailAddress
from dataclasses import dataclass
from typing import Optional
from django.contrib.auth import get_user_model

SIGNUP_INPUT_CLASS = "self-stretch px-3.5 py-2.5 bg-white rounded-lg shadow border border-gray-300 h-6 justify-start items-center gap-2 inline-flex grow shrink basis-0 text-gray-500 text-base font-normal font-sans leading-normal"


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = SIGNUP_INPUT_CLASS
        self.fields["email"].widget.attrs["class"] = SIGNUP_INPUT_CLASS
        self.fields["password1"].widget.attrs["class"] = SIGNUP_INPUT_CLASS
        self.fields["password2"].widget.attrs["class"] = SIGNUP_INPUT_CLASS
        self.fields["password2"].label = _("Confirm password")


class RememberPasswordWidget(forms.widgets.CheckboxInput):
    def render(self, name, value, attrs=None, renderer=None):
        checkbox_html = super().render(
            name,
            value,
            attrs={
                "class": attrs.get("class", "")
                + "rounded border border-gray-300 opacity-50 accent-green-500"
            },
            renderer=renderer,
        )
        checkbox_label = _("Remember me")
        checkbox_markup = f"""
            <div class="grow shrink basis-0 h-5 justify-start items-center gap-2 flex">
                {checkbox_html}
                <div class="grow shrink basis-0 flex-col justify-start items-center inline-flex">
                    <div class="self-stretch text-slate-700 text-sm font-medium font-sans leading-tight">
                        {checkbox_label}
                    </div>
                </div>
            </div>
        """
        return mark_safe(checkbox_markup)


class CustomLoginForm(LoginForm):
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "self-stretch px-3.5 py-2.5 bg-white rounded-lg shadow border border-gray-300 justify-start items-center gap-2 inline-flex grow shrink basis-0 h-6 flexgrow text-gray-800 text-base font-normal font-sans leading-normal",
                "placeholder": "••••••••",
            }
        ),
    )
    remember = forms.BooleanField(
        label=_("Remember Me"), required=False, widget=RememberPasswordWidget()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        try:
            reset_url = reverse("account_reset_password")
        except NoReverseMatch:
            pass
        else:
            forgot_txt = _("Forgot your password?")
            self.fields["password"].help_text = mark_safe(
                f'<a href="{reset_url}">{forgot_txt}</a>'
            )

        login_field = forms.CharField(
            label=_("Email"),
            required=True,
            widget=forms.TextInput(
                attrs={
                    "class": "self-stretch px-3.5 py-2.5 bg-white rounded-lg shadow border border-gray-300 justify-start items-center gap-2 inline-flex grow shrink basis-0 h-6 flexgrow text-gray-800 text-base font-normal font-sans leading-normal",
                    "placeholder": _("example@example.com"),
                    "autocomplete": "email",
                }
            ),
        )
        self.fields["login"] = login_field


class CustomResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "self-stretch px-3.5 py-2.5 bg-white rounded-lg shadow border border-gray-300 inline-flex h-6 justify-start items-center gap-2 grow shrink basis-0 text-gray-500 text-base font-normal font-sans leading-normal",
                "placeholder": _("example@example.com"),
                "autocomplete": "email",
                "type": "email",
            }
        ),
    )


@dataclass
class AccountChanges:
    email_address: Optional[EmailAddress] = None
    email_changed: bool = False


User = get_user_model()


class AccountForm(AddEmailForm):
    username = forms.CharField(
        label=_("Username"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "self-stretch px-3.5 py-2.5 bg-white rounded-lg shadow border border-gray-300 justify-start items-center gap-2 inline-flex grow shrink basis-0 h-6 text-gray-900 text-base font-normal font-sans leading-normal",
                "placeholder": _("Jon Snow"),
                "type": "text",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email address"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "self-stretch px-3.5 py-2.5 bg-white rounded-lg shadow border border-gray-300 justify-start items-center gap-2 inline-flex grow shrink basis-0 h-6 text-gray-900 text-base font-normal font-sans leading-normal",
                "placeholder": _("example@example.com"),
                "type": "email",
            }
        ),
    )
    phone = PhoneNumberField(
        region="PL",
        required=False,
        label=_("Phone Number"),
        widget=RegionalPhoneNumberWidget(
            attrs={
                "class": "self-stretch px-3.5 py-2.5 bg-white rounded-lg shadow border border-gray-300 justify-start items-center gap-2 inline-flex grow shrink basis-0 h-6 text-gray-900 text-base font-normal font-sans leading-normal",
                "placeholder": "+48 111 111 111",
                "type": "tel",
            }
        ),
    )

    def clean_email(self):
        if self.user.email != self.cleaned_data["email"]:  # means user changed email
            return super().clean_email()
        return self.user.email

    def clean_username(self):
        errors = {"username_taken": "This username is already taken"}
        value = self.cleaned_data["username"]
        if self.user.username != value:
            if User.objects.filter(username=value).exists():
                raise forms.ValidationError(errors["username_taken"])
            return value
        return self.user.username

    def save(self, request):
        changes = AccountChanges()
        if self.is_valid():
            if self.user.email != self.cleaned_data["email"]:
                email_address = EmailAddress.objects.add_new_email(
                    request, self.user, self.cleaned_data["email"]
                )
                changes.email_changed = True
                changes.email_address = email_address

            if self.user.username != self.cleaned_data["username"]:
                self.user.username = self.cleaned_data["username"]

            if self.user.phone_number != self.cleaned_data["phone"]:
                self.user.phone_number = self.cleaned_data["phone"]

            self.user.save()

        return changes
