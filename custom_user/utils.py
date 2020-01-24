from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from zxcvbn import zxcvbn

def clean_password(password):
    zxcvbn_enabled = getattr(settings, 'CUSTOM_USER_ENABLE_ZXCVBN', True)
    if zxcvbn_enabled:
        user_inputs = [
            'doubleh',
            #possibly include user fields like the user's email address and name
        ]
        ps = zxcvbn(password, user_inputs=user_inputs)
        if password and ps['score'] < 2:   # the score is from 0 to 4. 4 being the most secure.
            raise forms.ValidationError(
                "The password does not meet security requirements.",
                code='password_insecure',
            )

        # as an added measure, consider checking the password against existing passwords in the database.
        # https://diogomonica.com/posts/password-security-why-the-horse-battery-staple-is-not-correct/

    else:
        validate_password(password, user=None)

    return password
