from django.conf.urls import *

urlpatterns = patterns('socialnetwork.account.views',
                       url(r'^account/$', 'account'),
                       url(r'^account/login/$', 'login'),
                       url(r'^account/logout/$', 'logout'),
                       url(r'^account/register/$', 'register'),
                       url(r'^account/user-icon/$', 'user_icon'),

)
