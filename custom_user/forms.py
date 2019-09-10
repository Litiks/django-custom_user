"""EmailUser forms."""
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import LoginForm
from captcha.fields import CaptchaField

from custom_user.utils import clean_password

class EmailUserCreationForm(forms.ModelForm):
    """ A form for creating new users.

        Includes all the required fields, plus a repeated password.
    """

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_insecure': _("The password does not meet security requirements."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password_js = """
        <span id='id_password1_help'></span>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/zxcvbn/1.0/zxcvbn.js'></script>
        <script>
            var input = document.getElementById('id_password1');
            var help = document.getElementById('id_password1_help');
            input.addEventListener('keyup', function(){
                analysis = zxcvbn(input.value);
                score = analysis.score;
                if(score == 0){
                    score_text = 'too weak';
                    score_style = 'color:red;'
                }else if(score == 1){
                    score_text = 'too weak';
                    score_style = 'color:red;'
                }else if(score == 2){
                    score_text = 'weak';
                    score_style = 'color:green;'
                }else if(score == 3){
                    score_text = 'good';
                    score_style = 'color:green;'
                }else if(score == 4){
                    score_text = 'great';
                    score_style = 'color:green;'
                }
                if(score_text=='too weak'){
                    try {
                        dictionary_name = analysis.match_sequence[0].dictionary_name
                        if (dictionary_name){
                            score_text += " - common " + dictionary_name
                        }
                    }catch(err) {
                        // do nothing
                    }
                }
                help.innerHTML = "<span style='"+score_style+"'>Security Score: " + score_text + "</span>"
            })
        </script>
    """
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_("Your password cannot be based on a single english word, or keyboard pattern." + password_js.replace("", "")))
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

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
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        return clean_password(password1)

    def clean_password2(self):
        """Check that the two password entries match.

        :return str password2: cleaned password2
        :raise forms.ValidationError: password2 != password1

        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        """Save user.

        Save the provided password in hashed format.

        :return custom_user.models.EmailUser: user

        """
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EmailUserChangeForm(forms.ModelForm):
    """ A form for updating users.

        Includes all the fields on the user, but replaces the password field
        with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

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

class CaptchaLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CaptchaLoginForm, self).__init__(*args, **kwargs)
        self.fields['captcha'] = CaptchaField()

        # dirty re-ordering of fields.
        if 'remember' in self.fields:
            r = self.fields['remember']
            del(self.fields['remember'])
            self.fields['remember'] = r
