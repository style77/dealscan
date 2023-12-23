from unittest.mock import ANY

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from allauth.account.authentication import AUTHENTICATION_METHODS_SESSION_KEY
from allauth.account.models import EmailAddress
from django.test import TestCase


class LoginFormTestTest(TestCase):
    def test_username_containing_at(self):
        user = get_user_model().objects.create(username="testuser3", email="test@example.com")
        user.set_password("supersecret")
        user.save()
        EmailAddress.objects.create(
            user=user,
            email="test@example.com",
            primary=True,
            verified=True,
        )
        resp = self.client.post(
            reverse("account_login"),
            {"login": "testuser3", "password": "supersecret"},
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )
        self.assertEqual(
            self.client.session[AUTHENTICATION_METHODS_SESSION_KEY],
            [
                {
                    "at": ANY,
                    "username": "testuser3",
                    "method": "password",
                }
            ],
        )

    def test_redirect_when_authenticated(self):
        password = "doe"
        user = get_user_model().objects.create(username="john", email="test@example.com", is_active=True)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        self.client.force_login(user)
        c = self.client
        resp = c.get(reverse("account_login"))
        self.assertRedirects(resp, "/dashboard", fetch_redirect_response=False)

    def test_login_unverified_account_optional(self):
        """Tests login behavior when email verification is optional."""
        user = get_user_model().objects.create(username="john", email="test@example.com")
        user.set_password("doe")
        user.save()
        EmailAddress.objects.create(
            user=user, email="user@example.com", primary=True, verified=False
        )
        resp = self.client.post(
            reverse("account_login"), {"login": "john", "password": "doe"}
        )
        self.assertRedirects(
            resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

    # def test_login_inactive_account(self):
    #     """
    #     Tests login behavior with inactive accounts.

    #     Inactive user accounts should be prevented from performing any actions,
    #     regardless of their verified state.
    #     """
    #     # Inactive and verified user account
    #     user = get_user_model().objects.create(username="john", email="test@example.com", is_active=False)
    #     user.set_password("doe")
    #     user.save()
    #     EmailAddress.objects.create(
    #         user=user, email="john@example.com", primary=True, verified=True
    #     )
    #     resp = self.client.post(
    #         reverse("account_login"), {"login": "john", "password": "doe"}
    #     )
    #     self.assertRedirects(resp, reverse("account_inactive"))

    #     # Inactive and unverified user account
    #     user = get_user_model().objects.create(username="doe", email="test2@example.com", is_active=False)
    #     user.set_password("john")
    #     user.save()
    #     EmailAddress.objects.create(
    #         user=user, email="user@example.com", primary=True, verified=False
    #     )
    #     resp = self.client.post(
    #         reverse("account_login"), {"login": "doe", "password": "john"}
    #     )
    #     self.assertRedirects(resp, reverse("account_inactive"))
