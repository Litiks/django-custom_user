"""User models."""
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class EmailUserManager(BaseUserManager):

    """Custom manager for EmailUser."""

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email is not set

        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user

        """
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user

        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    """
        Abstract User with the same behaviour as Django's default User.

        AbstractEmailUser does not have username field. Uses email as the
        USERNAME_FIELD for authentication.

        Use this if you need to extend EmailUser.

        Inherits from both the AbstractBaseUser and PermissionMixin.

        The following attributes are inherited from the superclasses:
            * password
            * last_login
            * is_superuser
    """

    email = models.EmailField(_('email address'), max_length=255,
                              unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """Return the email."""
        return self.email

    def get_short_name(self):
        """Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        """ We modify django's default behaviour here, for our own sanity.

            Default behaviour:
            see: https://docs.djangoproject.com/en/1.9/ref/contrib/auth/#django.contrib.auth.models.User.has_perm
            "If obj is passed in, this method won't check for a permission for the model, but for this specific object."

            We just want to know if Bill can access Bob. 
                With the current behaviour, we need to do this by first asking "can Bill access people?"
                And then (if no), asking if Bill can access Bob specifically.

            Django Guardian is aware of this behaviour, and they suggest that you just avoid the use of has_perm. 
                see: http://django-guardian.readthedocs.io/en/stable/userguide/check.html#inside-views

            But that's stupid.
        """
        result = super(AbstractEmailUser, self).has_perm(perm, obj)
        if obj and not result:
            # Try again without object. (this will check group permissions)
            result = super(AbstractEmailUser, self).has_perm(perm)
        return result

class EmailUser(AbstractEmailUser):
    """
        Concrete class of AbstractEmailUser.

        Use this if you don't need to extend EmailUser.
    """

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'
