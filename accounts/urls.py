from allauth.account.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from accounts.views import (
    MyConfirmEmailView,
    MyEmailView,
    MyLoginView,
    MyPasswordResetDoneView,
    MyPasswordResetFromKeyDoneView,
    MyPasswordResetFromKeyView,
    MyPasswordResetView,
    MySignupView,
    VerificationEmailSent,
)

urlpatterns = [
    path(r"login/", MyLoginView.as_view(), name="account_login"),
    path(r"signup/", MySignupView.as_view(), name="account_signup"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path("", login_required(MyEmailView.as_view()), name="account"),
    path(
        "confirm-email/",
        VerificationEmailSent.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        MyConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        r"password/reset/", MyPasswordResetView.as_view(), name="account_reset_password"
    ),
    path(
        r"password/reset/done/",
        MyPasswordResetDoneView.as_view(),
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        MyPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        MyPasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done",
    ),
]
