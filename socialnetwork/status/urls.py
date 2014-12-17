from django.conf.urls import *

urlpatterns = patterns('socialnetwork.status.views',
                        url(r'^people/(?P<people_url>\d{1,100})/status/create/$', 'status_create'),
                        url(r'^people/(?P<people_url>\d{1,100})/status/(?P<status_url>\d{1,100})/$', 'status'),
                        url(r'^people/(?P<people_url>\d{1,100})/status/(?P<status_url>\d{1,100})/comment$', 'status_comment'),
                        url(r'^people/(?P<people_url>\d{1,100})/status/(?P<status_url>\d{1,100})/ret$', 'status_ret'),
                      )
