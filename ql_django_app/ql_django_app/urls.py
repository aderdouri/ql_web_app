"""
URL configuration for ql_django_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bond/', include('bond.urls')),
    path('swap/', include('swap.urls')),
    path('swaption/', include('swaption.urls')),
    path('european_option/', include('european_option.urls')),
    path('american_option/', include('american_option.urls')),
    path('bond02/', include('bond02.urls')),
    path('dateadder/', include('dateadder.urls')),

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]