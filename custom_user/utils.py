from django import forms
from zxcvbn import password_strength

def clean_password(password):
        user_inputs = [
            'doubleh',
            #possibly include user fields like the user's email address and name
        ]
        ps = password_strength(password, user_inputs)
        if password and ps['score'] < 2:   # the score is from 0 to 4. 4 being the most secure.
            raise forms.ValidationError(
                "The password does not meet security requirements.",
                code='password_insecure',
            )

        # as an added measure, consider checking the password against existing passwords in the database.
        # https://diogomonica.com/posts/password-security-why-the-horse-battery-staple-is-not-correct/

        return password

