# adapted from: https://github.com/guhan94/django-hibp-validator/blob/master/src/django-validator.py

import requests
import hashlib

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

# Set up a session, to enable connection pooling and reduce the dns / https overhead.
requests_session = requests.Session()

class PwnedValidator(object):
    def __init__(self, pwned_result_on_communication_error=False):
        # How to handle a communication error with hibp
        # Default is False (consider the password "not pwned")
        self.pwned_result_on_communication_error = pwned_result_on_communication_error

    @staticmethod
    def hash_password(password):
        hash_val = hashlib.sha1(password.encode('utf-8'))
        return hash_val.hexdigest().__str__()

    def _get_password_range(self, hash_index):
        # Querying HIBP for a range of password hashes by k-Anonymity model.
        headers = {
            # 'Add-Padding': 'true',              # ensure that every response returns a similary sized response.
            'User-Agent': 'django-custom_user',
        }
        with requests_session.get(f'https://api.pwnedpasswords.com/range/{hash_index}', headers=headers, timeout=5) as response:
            response.raise_for_status()
            return response.text

    def is_pwned(self, password):
        password_hash = self.hash_password(password)
        index = password_hash[0:5].upper()

        try:
            hash_list = self._get_password_range(hash_index=index)
        except:
            # A communication error has occurred.
            return self.pwned_result_on_communication_error

        hash_list = hash_list.splitlines()
        for h in hash_list:
            h = index + h
            h, count = h.split(':')
            if password_hash.upper() == h and int(count) > 0:
                # Oops given password is indeed pwned!
                return True
        # No hash matches found for the given password hash
        return False

    def validate(self, password, user=None):
        if self.is_pwned(password=password):
            raise ValidationError(
                _("This password was compromised in a data breach of another website or service, and is not considered safe."),
                code='password_compromised',
            )

    def get_help_text(self):
        return _(
            "Your password should not be re-used between different websites."
        )

class CautiousPwnedValidator(PwnedValidator):
    """ Same as PwnedValidator, but if there's a communication error, consider the password unsafe. """
    def __init__(self):
        super().__init__(pwned_result_on_communication_error=True)
