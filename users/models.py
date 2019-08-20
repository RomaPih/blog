import hashlib
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.core.signing import Signer, TimestampSigner
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _, ugettext


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Create and save a user with the given email, and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a user with the given email, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    @classmethod
    def normalize_phone(cls, phone):
        """Normalize the phone number by lowercasing the domain part of it."""
        import re
        phone = phone or ''
        re.sub('\D', '', phone)
        if len(phone) == 11:
            return '3' + phone
        elif len(phone) == 10:
            return '38' + phone
        else:
            return phone


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), max_length=150, unique=True)
    phone = models.CharField(_('phone number'), max_length=100, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    confirmed_registration = models.BooleanField(_('confirmed registration'), default=True)
    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        """Redefine default clean method."""
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.phone = self.__class__.objects.normalize_phone(self.phone)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_last_login_hash(self):
        # return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:8]
        return hashlib.md5(self.last_login.strftime('%Y-%m-%d-%H-%M-%S-%f').encode('utf-8')).hexdigest()[:8]

    def send_registration_email(self):
        url = 'http://{}{}'.format(
            Site.objects.get_current().domain,
            reverse('registration_confirm', kwargs={'token': Signer(salt='registration-confirm').sign(self.pk)})
        )
        self.email_user(
            ugettext('Підтвердіть реєстрацію'),
            ugettext('Для підтвердження перейдіть по ссилці {}'.format(url))
        )

    def send_password_recovery_email(self):
        data = '{}:{}'.format(self.pk, self.get_last_login_hash())
        token = TimestampSigner(salt='recovery-password-form').sign(data)
        url = 'http://{}{}'.format(
            Site.objects.get_current().domain,
            reverse('recovery_password_form', kwargs={'token': token})
        )
        self.email_user(
            ugettext('Підтвердіть відновлення паролю'),
            ugettext('Для підтвердження перейдіть по ссилці {}'.format(url))
        )
