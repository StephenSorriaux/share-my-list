"""xmas_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from lists.views import logout_view

urlpatterns = [
    path('', include('lists.urls')),
    path('admin/', admin.site.urls),
    url(  
        r'^login/$',  
        LoginView.as_view(
            template_name='admin/login.html',
            extra_context={         
              'title': 'Login',
              'site_title': 'My Site',
              'site_header': 'My Site Login'}),
        name='login'),
    url(  
        r'^logout/$',  
        logout_view,
        name='logout'),   
]
