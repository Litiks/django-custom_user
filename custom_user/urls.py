from django.conf.urls import url, include
from custom_user import views

urlpatterns = [
    url(r"^login/$", views.login, name="account_login"),
    url(r"^login/$", views.login, name="login"),
    url(r'^', include('allauth.urls')),
]

# some handling for older versions of django (pre 1.8)
# I'm not sure that this is actually necessary.. Please message aaron@litiks.com if you need this.
# try:
#     from django.conf.urls import patterns
#     urlpatterns = patterns("", *urlpatterns)
# except:
#     pass
