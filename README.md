# django-custom_user
A custom django user model, with some basic enhancements

Features:
- email based login and account management
- email verification (using allauth)
- social logins (using allauth)

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
2. Follow instructions to [configure django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)
3. settings.py:
```python
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
```
4. urls.py:
```
urlpatterns = [
    ...
    url(r'^accounts/', include('custom_user.urls')),
    ...
]
```
5. If you want to automatically revoke pwned passwords: settings.py
```python
# Specific to custom_user.
# These validators are checked during login (rather than when the password is set)
# If a password fails any of these validators; we perform an email verification.
CUSTOM_USER_LOGIN_PASSWORD_VALIDATORS = [
    {"NAME": "custom_user.password_validation.PwnedValidator"},
]
```
6. If you want weak passwords to fall back to email-based login: settings.py
```python
ACCOUNT_LOGIN_BY_CODE_ENABLED = True       # enable login by emailed code.

# disable password validation on creation, to allow users to set a weak password
AUTH_PASSWORD_VALIDATORS = [
    # {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    # {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    # {"NAME": "custom_user.password_validation.PwnedValidator"},
]

# Specific to custom_user.
# These validators are checked during login (rather than when the password is set)
# If a password fails any of these validators; we perform an email verification.
CUSTOM_USER_LOGIN_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "custom_user.password_validation.CautiousPwnedValidator"},
]
```
