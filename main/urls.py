from django.urls import path
from . import views as v

app_name = "main"

urlpatterns = [
    path('', v.home, name='home'),
    path('logout/', v.logout, name='logout')
]

handler400 = 'main.views.page_not_found'