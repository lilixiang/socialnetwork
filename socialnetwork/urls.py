from django.conf.urls import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socialnetwork.views.home', name='home'),
    # url(r'^socialnetwork/', include('socialnetwork.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('socialnetwork.account.urls')),
    url(r'', include('socialnetwork.people.urls')),
    url(r'', include('socialnetwork.note.urls')),
    url(r'', include('socialnetwork.status.urls')),
    url(r'', include('socialnetwork.feed.urls')),
    url(r'', include('socialnetwork.board.urls')),
    url(r'', include('socialnetwork.album.urls')),


)

