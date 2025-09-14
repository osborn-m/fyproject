from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    VerifyEmailView,
    ResetPasswordRequestView,
    ResetPasswordConfirmView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='accounts-register'),
    path('login/', TokenObtainPairView.as_view(), name='accounts-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/<uidb64>/<token>/', VerifyEmailView.as_view(), name='accounts-verify'),
    path('password-reset/', ResetPasswordRequestView.as_view(), name='accounts-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='accounts-password-reset-confirm'),
]
