from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from views import *

urlpatterns = patterns('',
    url(r'^$', main, name='main'),
    url(r'^bookmarklet/$', bookmarklet, name='bookmarklet'),
    url(r'^token/$', token, name='token'),
    url(r'^delete/device/$', delete_device, name='delete_device'),
    url(r'^delete/url/$', delete_url, name='delete_url'),
    url(r'^accounts/login/$', login, name='login'),
)
