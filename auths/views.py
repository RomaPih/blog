from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from auths.forms import RegistarionForm


class RegistrationView(TemplateView):
    template_name = 'registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        self.form = RegistarionForm(request.POST or None)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save()
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class LoginView(TemplateView):
    template_name = 'login.html'


class RecoveryPasswordView(TemplateView):
    template_name = 'recovery_password.html'


