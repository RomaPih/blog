from django.contrib.auth.views import LogoutView
from django.urls import path

from auths.views import RegistrationView, LoginView
from auths.views import RecoveryPasswordView
from auths.views import RegistrationConfirmView
from auths.views import PasswordRecoveryConfirmView
from django.conf import settings

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/(<token>.+)', RegistrationConfirmView.as_view(), name='registration_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': '/'}, name='auth_logout'),
    path('recovery_password/', RecoveryPasswordView.as_view(), name='recovery_password'),
    path('recovery_password/(<token>.+)', PasswordRecoveryConfirmView.as_view(), name='recovery_password_form'),
]