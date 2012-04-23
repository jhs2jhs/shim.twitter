from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from s_twitter import t_conn, f_conn

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 's_twitter.views.home', name='home'),
    # url(r'^s_twitter/', include('s_twitter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 's_twitter.views.list_shims'),

    #url(r'^t_conn/hello', 'hello', include('s_twitter.t_conn.views')),
    url(r'^t_conn/hello', 't_conn.test.hello'),
    url(r'^t_conn/test_oauth', 't_conn.test.test_oauth2'),
    url(r'^t_conn/test_tweepy', 't_conn.test.test_tweepy'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    url(r'^oauth/request/?$', 't_conn.views.twitter_oauth_request'),
    url(r'^oauth/authenticated/?$', 't_conn.views.twitter_oauth_authenticated'),

    # other twitter api should be trieve here
    url(r'^shim/(?P<t_user_id>\d+)/', 't_conn.views.user_timeline'),

    # facebook session
    url(r'^oauth/facebook/init/?$', 'f_conn.views.facebook_oauth_init'),
    url(r'^oauth/facebook/request/?$', 'f_conn.views.facebook_oauth_request'),
    url(r'^oauth/facebook/authenticated/?$', 'f_conn.views.facebook_oauth_authenticated'),
    url('^shim/facebook/(?P<f_user_id>\d+)/', 'f_conn.views.user_photo_tagged'),
)
