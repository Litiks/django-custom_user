# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
  name='django-custom_user',
  description='A custom django user model, with some basic enhancements.',
  packages=['custom_user'],
  install_requires=[
    'django-allauth',
    'zxcvbn>=4',
    'django-ratelimit',
    'django-simple-captcha',
  ],
)
