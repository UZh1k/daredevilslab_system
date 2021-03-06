"""daredevilslabs_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from qrreader.views import *

urlpatterns = [
    path('', main),
    path('client_list', client_list),
    path('admin/', admin.site.urls),
    path('<int:course_id>', course),
    path('lesson/<int:lesson_id>', lesson),
    re_path(r'^(?P<lesson_url>[\w]{10})/$', check_in),
    re_path(r'^(?P<lesson_url>[\w]{10})/login', sign_in),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
