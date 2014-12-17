from django.conf.urls import *

urlpatterns = patterns('socialnetwork.people.views',
                       url(r'^people/(?P<people_url>\d{1,100})/$', 'people'),
                       url(r'^people/(?P<people_url>\d{1,100})/contact/list$', 'contact'),
                       url(r'^people/(?P<people_url>\d{1,100})/contact/rlist$', 'contact_r'),
                       url(r'^people/(?P<people_url>\d{1,100})/add$', 'people_add'),
                       url(r'^people/(?P<people_url>\d{1,100})/del$', 'people_del'),
                       url(r'^people/search/$', 'people_search'),

                       )
urlpatterns += patterns('socialnetwork.status.views',
                        url(r'^people/(?P<people_url>\d{1,100})/status/create/$', 'status_create'),
                        url(r'^people/(?P<people_url>\d{1,100})/status/(?P<status_url>\d{1,100})/$', 'status'),
                        url(r'^people/(?P<people_url>\d{1,100})/status/(?P<status_url>\d{1,100})/comment$', 'status_comment'),
                       )