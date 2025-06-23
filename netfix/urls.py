"""netfix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# netfix/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
# from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home + logout
    path('', include(('main.urls', 'main'), namespace='main')),

    # All auth under /accounts/
    path('accounts/', include(('users.urls', 'users'), namespace='users')),

    # Services
    path('services/', include(('services.urls', 'services'), namespace='services')),

]

# DEBUG LINE
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Static files routing (when DEBUG=False)
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, kwargs={'document_root': settings.STATIC_ROOT}),
    ]

# DEBUG LINE
# print(">>> STATIC ROUTE:", static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)) 

handler404 = views.page_not_found
