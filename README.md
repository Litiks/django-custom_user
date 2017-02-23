# django-custom_user
A custom django user model, with some basic enhancements

Features:
- email based login and account management
- email verification (using allauth)
- social logins (using allauth)
- password integrity checks using zxcvbn
- login attempt rate-limiting, enabling captcha

Generally, this app should conform to Django's guidelines: 
https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#specifying-a-custom-user-model


Install
-------

- using pip: `pip install https://github.com/Litiks/django-custom_user/archive/master.zip`
- or: add to your requirements.txt: `-e git+https://github.com/Litiks/django-custom_user.git#egg=django-custom_user`
- or: copy the 'custom_user' folder to your python working directory


Integrate
---------

1. Add 'custom_user' to your settings.INSTALLED_APPS
2. Add to your settings:

```
# custom_user (Custom User Model):
# https://docs.djangoproject.com/en/1.8/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'custom_user.EmailUser'


# allauth
# http://django-allauth.readthedocs.org/en/latest/installation.html
# You can adjust these settings to your hearts content
SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True     # remember credentials for 3 weeks
ACCOUNT_LOGOUT_ON_GET = True        # don't show the logout confirmation. Just logout immediately.
ACCOUNT_ADAPTER = 'custom_user.adapter.MyAccountAdapter'
LOGIN_URL = "/"     # we change this, so that users see the Facebook login prompt, rather than the traditional username login page.
LOGIN_REDIRECT_URL = "/"    # this isn't really an allauth-related setting
```

