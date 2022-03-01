from django.urls import include, path

from custom_user import views

urlpatterns = [
    path('login/', views.login, name="account_login"),
    path('login/', views.login, name="login"),
    path('', include('allauth.urls')),
]
