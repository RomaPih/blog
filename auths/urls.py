from django.urls import path

from auths.views import RegistrationView, LoginView
from auths.views import RecoveryPasswordView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('lorecovery_password/', RecoveryPasswordView.as_view(), name='recovery_password'),
]