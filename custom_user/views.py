from django.shortcuts import render

from allauth.account.views import LoginView
from ratelimit.decorators import ratelimit

from custom_user.forms import CaptchaLoginForm

class MyLoginView(LoginView):
    def get_form_class(self):
        # disabling allauth's fetcher from settings.
        return self.form_class

allauth_login_view = MyLoginView.as_view()
captcha_login_view = MyLoginView.as_view(form_class=CaptchaLoginForm)

@ratelimit(key='ip', rate='500/m', method=ratelimit.UNSAFE)
@ratelimit(key='post:username', rate='5/m', method=ratelimit.UNSAFE)
@ratelimit(key='post:password', rate='5/m', method=ratelimit.UNSAFE)
def login(request, *args, **kwargs):
    if getattr(request, 'limited', False):
        v = captcha_login_view
    else:
        v = allauth_login_view
    return v(request, *args, **kwargs)
