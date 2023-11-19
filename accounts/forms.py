from allauth.account.forms import LoginForm, ResetPasswordForm
from django import forms
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


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
