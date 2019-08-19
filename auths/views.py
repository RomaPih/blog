from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.signing import Signer, BadSignature
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from auths.forms import RegistarionForm
from users.models import User
from django.utils.translation import ugettext_lazy as _
from mysite import settings
from auths.forms import LoginForm


class RegistrationView(TemplateView):
    template_name = 'registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        self.form = RegistarionForm(request.POST or None)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['form'] = self.form
        if 'registered_user_id' in self.request.session:
            context['registered_user'] = User.objects.get(pk=self.request.session.pop('registered_user_id'))
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save()
            user.send_registration_email()
            request.session['registered_user_id'] = user.pk
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy(settings.LOGIN_URL)
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404
        try:
            user_id = Signer(salt='registration-confirm').unsign(kwargs['token'])
        except BadSignature:
            raise Http404
        user = User.objects.get(pk=user_id)
        if user.confirmed_registration:
            raise Http404
        user.confirmed_registration = True
        user.save(update_fields=('confirmed_registration',))
        messages.success(request, _('Ваша реєстрація успішно виконана.'))
        return super(RegistrationConfirmView, self).dispatch(request, *args, **kwargs)


class LogInView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        return LoginView(request, authentication_form=LoginForm)


class RecoveryPasswordView(TemplateView):
    template_name = 'recovery_password.html'


