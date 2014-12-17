from django.conf.urls import *

urlpatterns = patterns('socialnetwork.board.views',
    url(r'^people/(?P<people_url>\d{1,100})/board/$', 'board'),


)
