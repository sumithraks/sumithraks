from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify-email"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("2fa/verify/", views.TwoFactorVerifyView.as_view(), name="2fa-verify"),
    path("2fa/enroll/", views.TwoFactorEnrollView.as_view(), name="2fa-enroll"),
    path("2fa/confirm/", views.TwoFactorConfirmView.as_view(), name="2fa-confirm"),
    path("2fa/disable/", views.TwoFactorDisableView.as_view(), name="2fa-disable"),
    path("password-reset/request/", views.PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset/confirm/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("me/", views.MeView.as_view(), name="me"),
]
