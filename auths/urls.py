from django.urls import path

from auths.views import RegistrationView, LoginView
from auths.views import RecoveryPasswordView
from auths.views import RegistrationConfirmView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/(<token>.+)', RegistrationConfirmView.as_view(), name='registration_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('lorecovery_password/', RecoveryPasswordView.as_view(), name='recovery_password'),
]