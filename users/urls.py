from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),

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

    path('login/', views.LoginUserView, name='login_user'),

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

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

    path('company/<str:username>/', views.company_profile, name='company_profile'),
]
