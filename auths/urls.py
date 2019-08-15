from django.urls import path

from auths.views import RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
]