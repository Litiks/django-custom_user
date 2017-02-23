""" 
    Custom user model for Django with email instead of username.
    This app is derived from: https://github.com/jcugat/django-custom-user
    It has been modified to include some special login handling (for password integrity).
"""

__version__ = '0.5'

default_app_config = 'custom_user.apps.CustomUserConfig'
