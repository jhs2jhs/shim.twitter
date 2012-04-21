from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from s_twitter import t_conn

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 's_twitter.views.home', name='home'),
    # url(r'^s_twitter/', include('s_twitter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^t_conn/hello', 'hello', include('s_twitter.t_conn.views')),
    url(r'^t_conn/hello', 't_conn.views.hello'),
    url(r'^t_conn/test_tweepy', 't_conn.views.test_tweepy')
)
