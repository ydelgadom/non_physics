"""catadb_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from catadb import views
import settings



urlpatterns = [
    url(r'^start/', views.start, name='start'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^welcome/([^/]+)', views.welcome, name='welcome'),
    url(r'^notes/([^/]+)/([^/]+)', views.new_tasting_note, name='new_tasting_note'),
    url(r'^old_notes/([^/]+)', views.old_notes, name='old_notes'),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^delete/([^/]+)/([^/]+)', views.delete_wine, name='delete_wine'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False),
        name="favicon"
    ),

]
