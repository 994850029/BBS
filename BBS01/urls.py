"""BBS01 URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.views.static import serve
from BBS01 import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'get_img/', views.get_img, name='get_img'),
    url(r'^register/$', views.register),
    url(r'^user_blur/', views.user_blur),
    url(r'^index/$', views.index),
    url(r'^$', views.index),
    url(r'^logout/$', views.user_logout),
    url(r'^setpwd/$', views.set_pwd),
    url(r'^img_update/', views.img_update),
    url(r'^set_re_password/', views.set_re_password),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^(?P<username>[\w]+)/(?P<condition>category|tag|archive)/(?P<id>.*)', views.user_blog),
    url(r'^(?P<username>[\w]+)/article/(?P<id>\d+)',views.article_content),
    url(r'^up_and_down/',views.up_and_down),
    url(r'^commit/',views.commit),
    url(r'^(?P<username>[\w]+)', views.user_blog),
]
