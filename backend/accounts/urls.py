from django.urls import path
from .views import CsrfView, CurrentUserView, LoginView, LogoutView, PasswordChangeView, RegistrationView

urlpatterns = [
    path("csrf/", CsrfView.as_view(), name="auth-csrf"),
    path("register/", RegistrationView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", CurrentUserView.as_view(), name="auth-me"),
    path("password/change/", PasswordChangeView.as_view(), name="auth-password-change"),
]
