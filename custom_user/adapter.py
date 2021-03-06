from __future__ import unicode_literals
# Custom adjustments to django-allauth

from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from custom_user.utils import clean_password as my_clean_password

class MyAccountAdapter(DefaultAccountAdapter):

    def clean_password(self, password, user=None):
        """ Validates a password. """
        return my_clean_password(password)
