from allauth.core import context
from allauth.utils import get_username_max_length
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

from accounts.forms import CustomSignupForm


class SignupFormTestTest(TestCase):
    def test_custom_form_field_order(self):
        expected_field_order = [
            "email",
            "username",
            "password1",
            "password2",
        ]

        form = CustomSignupForm()
        self.assertEqual(list(form.fields.keys()), expected_field_order)

    def test_username_not_in_blacklist(self):
        data = {
            "username": "theusername",
            "email": "user@example.com",
            "password1": "super-secret-PASSWORD",
            "password2": "super-secret-PASSWORD",
        }
        form = CustomSignupForm(data, email_required=True)
        self.assertTrue(form.is_valid())

    def test_username_in_blacklist(self):
        data = {
            "username": "admin",
            "email": "user@example.com",
            "password1": "super-secret-PASSWORD",
            "password2": "super-secret-PASSWORD",
        }
        form = CustomSignupForm(data, email_required=True)
        self.assertFalse(form.is_valid())

    def test_username_maxlength(self):
        data = {
            "username": "username",
            "email": "user@example.com",
            "password1": "super-secret-PASSWORD",
            "password2": "super-secret-PASSWORD",
        }
        form = CustomSignupForm(data, email_required=True)
        max_length = get_username_max_length()
        field = form.fields["username"]
        self.assertEqual(field.max_length, max_length)
        widget = field.widget
        self.assertEqual(widget.attrs.get("maxlength"), str(max_length))


class SignupTest(TestCase):
    def test_signup_password_twice_form_error(self):
        resp = self.client.post(
            reverse("account_signup"),
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpassword",
                "password2": "testpassword2",
            },
        )
        self.assertFormError(
            resp.context["form"],
            "password2",
            "You must type the same password each time.",
        )

    def test_signup(self):
        request = RequestFactory().post(
            reverse("account_signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )

        SessionMiddleware(lambda request: None).process_request(request)
        MessageMiddleware(lambda request: None).process_request(request)

        request.user = AnonymousUser()
        from allauth.account.views import signup

        with context.request_context(request):
            signup(request)

        user = get_user_model().objects.get(username="testuser")
        self.assertEqual(user.email, "test@example.com")

    def test_get_initial_with_valid_email(self):
        req = RequestFactory().get(
            f"{reverse('account_signup')}?email=test@example.com"
        )
        from allauth.account.views import signup

        SessionMiddleware(lambda request: None).process_request(req)
        req.user = AnonymousUser()
        with context.request_context(req):
            view = signup(req)
        assert view.context_data["view"].get_initial()["email"] == "test@example.com"

    def test_signup_without_email(self):
        response = self.client.post(
            reverse("account_signup"),
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertFormError(
            response.context["form"],
            "email",
            "This field is required.",
        )

    def test_signup_without_username(self):
        response = self.client.post(
            reverse("account_signup"),
            {
                "email": "test@example.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertFormError(
            response.context["form"],
            "username",
            "This field is required.",
        )

    def test_signup_with_existing_username(self):
        get_user_model().objects.create_user(
            username="testuser", email="test@example.com"
        )
        response = self.client.post(
            reverse("account_signup"),
            {"username": "testuser", "email": "test2@example.com"},
        )
        self.assertFormError(
            response.context["form"],
            "username",
            "A user with that username already exists.",
        )

    def test_signup_with_existing_email(self):
        get_user_model().objects.create_user(
            username="testuser", email="test@example.com"
        )
        response = self.client.post(
            reverse("account_signup"),
            {
                "username": "testuser2",
                "email": "test@example.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertFormError(
            response.context["form"],
            "email",
            "A user is already registered with this email address.",
        )
