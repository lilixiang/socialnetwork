from django.conf.urls import *

urlpatterns = patterns('socialnetwork.note.views',
                       url(r'^people/(?P<people_url>\d{1,100})/note/create/$', 'note_create'),
                       url(r'^people/(?P<people_url>\d{1,100})/notes/$', 'notes'),
                       url(r'^people/(?P<people_url>\d{1,100})/note/(?P<note_url>\d{1,100})/$', 'note'),
                       url(r'^people/(?P<people_url>\d{1,100})/note/(?P<note_url>\d{1,100})/edit/$', 'note_edit'),
                       url(r'^people/(?P<people_url>\d{1,100})/note/(?P<note_url>\d{1,100})/comment$', 'note_comment'),
                       url(r'^people/(?P<people_url>\d{1,100})/note/(?P<note_url>\d{1,100})/del', 'note_del'),

                       )
