from django import forms

from users.models import User
from django.utils.translation import ugettext_lazy as _


class RegistarionForm(forms.ModelForm):

    password1 = forms.CharField(label=_('пароль'), min_length=8, max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('повтор пароля'), min_length=8, max_length=30, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name')
    #
    # def __init__(self, *args, **kwargs):
    #     super(RegistarionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(RegistarionForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.confirmed_registration = False
        if commit:
            user.save()
        return user
