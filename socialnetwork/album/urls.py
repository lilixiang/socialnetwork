from django.conf.urls import *

urlpatterns = patterns('socialnetwork.album.views',
                       url(r'^photo/(?P<photo_url>\d{1,100})/$', 'photo'),
                       url(r'^photo/(?P<photo_url>\d{1,100})/comment$', 'photo_comment'),
                       url(r'^album/(?P<album_url>\d{1,100})/$', 'album'),
                       url(r'^album/create/$', 'album_create'),
                       url(r'^people/(?P<people_url>\d{1,100})/albums/$', 'album_list'),
                       url(r'^album/(?P<album_url>\d{1,100})/upload/$', 'photo_upload'),
                       url(r'^album/(?P<album_url>\d{1,100})/edit/$', 'album_edit'),



)
