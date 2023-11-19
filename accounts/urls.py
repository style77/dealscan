from django.urls import path
from accounts.views import MyLoginView, MySignupView, MyPasswordResetView, MyPasswordResetDoneView

urlpatterns = [
    path(r'login/', MyLoginView.as_view(), name='account_login'),
    path(r'signup/', MySignupView.as_view(), name='account_signup'),
    path(r'password_reset/', MyPasswordResetView.as_view(), name='account_reset_password'),
    path(r'password_reset_done/', MyPasswordResetDoneView.as_view(), name='account_reset_password_done'),
]