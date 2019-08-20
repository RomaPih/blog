from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.core import validators

from users.models import User
from django.utils.translation import ugettext_lazy as _, ugettext


class RegistarionForm(forms.ModelForm):

    password1 = forms.CharField(label=_('пароль'), min_length=8, max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('повтор пароля'), min_length=8, max_length=30, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name')

    def clean(self):
        data = super(RegistarionForm, self).clean()
        if 'password1' not in self.errors and 'password2' not in self.errors:
            if data['password1'] != data['password2']:
                self.add_error('password1', ugettext('Паролі не співпали'))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(ugettext('Користувач з таким email вже є.'))
        return email

    def save(self, commit=True):
        user = super(RegistarionForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.confirmed_registration = False
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self):
        super(LoginForm, self).__init__()

    def clean(self):
        has_error = False
        try:
            super(LoginForm, self).clean()
        except forms.ValidationError:
            has_error = True
        if has_error or self.errors or (self.user_cache and not self.user_cache.confirmed_registration):
            self._errors.clear()
            raise forms.ValidationError(ugettext('Неправильний email або пароль'))


class RecoveryPasswordForm(forms.Form):
    email = forms.EmailField(label=_('email'))

    def __init__(self, *args, **kwargs):
        super(RecoveryPasswordForm, self).__init__(*args, **kwargs)
        self._user = None

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self._user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_('Користувач з таким email не існує'))
        return email

    def get_user(self):
        return self._user


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        for field_name in ('new_password1', 'new_password2'):
            self.fields[field_name].validators.extend([validators.MinLengthValidator(8),
                                                      validators.MaxLengthValidator(40)])
