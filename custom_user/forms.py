from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm, ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

class EmailUserCreationForm(BaseUserCreationForm):
    """ A form for creating new users.

        Includes all the required fields, plus a repeated password.
    """
    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_email(self):
        """Clean form email.

        :return str email: cleaned email
        :raise forms.ValidationError: Email is duplicated

        """
        # Since EmailUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            "A user with that email already exists.",
            code='duplicate_email',
        )

class EmailUserChangeForm(forms.ModelForm):
    """ A form for updating users.

        Includes all the fields on the user, but replaces the password field
        with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = get_user_model()
        exclude = ()

    def __init__(self, *args, **kwargs):
        """Init the form."""
        super(EmailUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        """Clean password.

        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value.

        :return str password:

        """
        return self.initial["password"]
