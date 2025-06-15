# users/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'users'

urlpatterns = [
    # a simple “choose your flow” landing
    path('register/', views.register, name='register'),

    # two class-based signup flows
    path(
        'register/customer/',
        views.CustomerSignUpView.as_view(),
        name='register_customer'
    ),
    path(
        'register/company/',
        views.CompanySignUpView.as_view(),
        name='register_company'
    ),

    # login is a function, so don’t call as_view()
    path('login/', views.LoginUserView, name='login_user'),

    # built-in logout view
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # profile pages (must match your view function names & signatures)
    path(
        'customer/<str:username>/',
        views.customer_profile,
        name='customer_profile'
    ),
    path(
        'company/<str:username>/',
        views.company_profile,
        name='company_profile'
    ),
]
