# netfix/users/urls.py

from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # authentication
    path('login/',                   views.LoginUserView,             name='login_user'),
    path('register/customer/',       views.CustomerSignUpView.as_view(), name='register_customer'),
    path('register/company/',        views.CompanySignUpView.as_view(),  name='register_company'),

    # profiles
    path('customer/<slug:name>/',    views.customer_profile,          name='customer_profile'),
    path('company/<slug:name>/',     views.company_profile,           name='company_profile'),
]
