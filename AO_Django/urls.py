"""AO_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from AO_Django import views as ao
from Equipment import views as eq

urlpatterns = [
    path('', ao.menu, name='menu'),
    path('admin/', admin.site.urls),
    path('efficient/', eq.list_efficient_items,
         name='list_efficient_items'),
    path('efficient/<str:market>/', eq.list_efficient_items,
         name='list_efficient_items_market'),
    path('efficient/<int:id>/<str:market>/', eq.list_efficient_items,
         name='list_efficient_items_individual'),
    re_path(r'^efficient/(?P<id>\d+)/(?P<market>[ \w]+)/(?P<min_ip>[ \-\d]+)/$', eq.list_efficient_items,
            name='list_efficient_items_individual_min_ip'),
]
