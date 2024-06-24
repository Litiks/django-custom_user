from allauth.account.internal import flows
from allauth.account.views import LoginView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.shortcuts import redirect
from django.urls import reverse

from .models import EmailUser
from .password_validation import PwnedValidator

class MyLoginView(LoginView):
    def form_valid(self, form):
        if hasattr(settings,'CUSTOM_USER_LOGIN_PASSWORD_VALIDATORS'):
            # validating the password at login (rather just than at creation), allows us to raise alarm bells when a password is later determined to be weak (ex: in the case that it's been compromised)

            email = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = form.user

            # Sanity check: ensure that form.user's email address matches the submitted email.
            # Adding this while I scratch my head about https://litiks.sentry.io/issues/5526022591/, where EmailUser.objects.get() was failing here, because:
            # - There was no user account with a matching email address
            # - But the login form was somehow valid??
            # It's as though the form validation logic selected a different user account than I'd expect?
            if form.user.email != email:
                raise Exception("emails do not match??")

            # run it through the PwnedValidator
            # TODO run it through ALL of the validators..
            validators = get_password_validators(settings.CUSTOM_USER_LOGIN_PASSWORD_VALIDATORS)

            try:
                validate_password(password, user=user, password_validators=validators)
            except:
                # Validation failed.
                if hasattr(settings,'ACCOUNT_LOGIN_BY_CODE_ENABLED'):
                    # Send them an email code
                    flows.login_by_code.request_login_code(self.request, email)
                    # TODO:" set next here?"
                    return redirect(reverse("account_confirm_login_code"))
                else:
                    # Display a message and prompt the user to reset their password.
                    messages.add_message(self.request, messages.ERROR, "Your password no longer meets our security requirements. You'll need to reset your password.")
                    return redirect(reverse("account_reset_password"))

        return super().form_valid(form)
