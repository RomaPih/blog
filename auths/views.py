from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class RegistrationView(TemplateView):
    template_name = 'registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            ...