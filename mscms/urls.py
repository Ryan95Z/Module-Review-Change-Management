"""mscms URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from core.views import DashboardView, LoginView, LogoutView

urlpatterns = [
    # core view that is the route of the application
    url(r'^$', login_required(DashboardView.as_view()), name='dashboard'),
    url(r'^admin/', include('core.urls.admin')),
    url(r'^admin/', include('forms.urls.admin')),
    url(r'^module_leader/', include('forms.urls.module_leader')),
    url(r'^user/', include('core.urls.user')),
    url(r'^modules', include('core.urls.module_leader')),

    # admin panel route
    url(r'^admin/login/$', LoginView.as_view()),
    url(r'^admin/logout/$', LogoutView.as_view()),
    url(r'^admin/', admin.site.urls),

    # timeline urls
    url(r'timeline/', include('timeline.urls.timeline')),
]
