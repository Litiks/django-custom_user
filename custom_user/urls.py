from django.urls import include, path

from custom_user import views

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name="account_login"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('', include('allauth.urls')),
]
