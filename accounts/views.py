from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

# ------------------------------------------------------------------
# Registration (creates inactive user + sends verification email)
# ------------------------------------------------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        # generate token & uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # NOTE: change frontend host to your Next.js domain
        verify_url = f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/verify/{uid}/{token}/"

        subject = 'Verify your account'
        message = f'Welcome {user.username}!\n\nPlease verify your email by clicking the link below:\n\n{verify_url}\n\nIf you did not sign up, ignore this email.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

# ------------------------------------------------------------------
# Email verification endpoint
# ------------------------------------------------------------------
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------
# Password reset: request (sends email with link)
# ------------------------------------------------------------------
class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'email': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do not reveal whether the email exists; respond success for privacy
            return Response({'detail': 'If an account with that email exists, you will receive a reset link.'}, status=status.HTTP_200_OK)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/reset-password/{uid}/{token}/"

        subject = 'Password reset requested'
        message = f'Hi {user.username},\n\nUse the link below to reset your password:\n\n{reset_url}\n\nIf you did not request a password reset, ignore this email.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

        return Response({'detail': 'If an account with that email exists, you will receive a reset link.'}, status=status.HTTP_200_OK)

# ------------------------------------------------------------------
# Password reset confirm (frontend calls this with new password)
# POST body: { "password": "newpass" }
# ------------------------------------------------------------------
class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get('password')
        if not password:
            return Response({'password': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
