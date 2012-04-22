# Create your views here.
from django.shortcuts import HttpResponse, render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import Template, RequestContext
from django.core.context_processors import csrf
import json
import oauth2 as oauth
import myutil
import cgi
from t_conn.models import Profile, Consumer
import urllib #only use it to encode http url paramater, not use it for http connection


@login_required()
def twitter_list(request):
    user = request.user
    twitters = Profile.objects.filter(user=user)
    print twitters
    for t in twitters:
        print t.oauth_screen_name
    #views.login(request)
    c = RequestContext(request, {'profiles':twitters})
    return render_to_response('list_twitter.html', c)
    #return render_to_response('base.html', c)

    
#print settings.twitter_request_token_url
oauth_callback = urllib.urlencode({'oauth_callback':'http://localhost:8080/oauth/authenticated/'})

def get_consumer():
    token = settings.TWITTER_CONSUMER_TOKEN
    secret = settings.TWITTER_CONSUMER_SECRET
    consumer_objs = Consumer.objects.get_or_create(token=token, secret=secret)
    consumer_oauth = oauth.Consumer(token, secret)
    return consumer_oauth, consumer_objs[0]


@login_required
def twitter_oauth_request(request):
    #step 0: get consumer_oauth
    consumer_oauth, consumer_obj = get_consumer()
    client = oauth.Client(consumer_oauth)
    print consumer_obj

    #step 1: get a request token from twitter
    resp, content = client.request(settings.TWITTER_REQUEST_TOKEN_URL, 'POST', body=oauth_callback)
    #resp, content = client.request(settings.TWITTER_REQUEST_TOKEN_URL, 'GET')
    if resp['status'] != '200':
        print content
        raise Exception('Invalid response from Twitter')

    #step 2: store the request token in a session for later use
    request.session['request_token'] = dict(cgi.parse_qsl(content))
    print request.session['request_token']
    print resp

    #step 3: redirect the user to the authenticate URL. 
    url = '%s?oauth_token=%s'%(settings.TWITTER_AUTHENTICATE_URL, request.session['request_token']['oauth_token'])
    #url = '%s?oauth_token=%s&%s'%(settings.TWITTER_AUTHORIZE_URL, request.session['request_token']['oauth_token'], oauth_callback)
    print url

    return HttpResponseRedirect(url)

def twitter_oauth_authenticated(request):
    #step 0: get consumer_obj
    consumer_oauth, consumer_obj = get_consumer()
    client = oauth.Client(consumer_oauth)

    #step 1: use the request token in the session to build a new client. 
    print request.session['request_token']
    token = oauth.Token(request.session['request_token']['oauth_token'], request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer_oauth, token)
    
    #step 2: request the authorized access token from Twitter
    resp, content = client.request(settings.TWITTER_ACCESS_TOKEN_URL, 'GET')
    if resp['status'] != '200':
        raise Exception ('Invalid response from twitter')
    access_token = dict(cgi.parse_qsl(content))
    #print content
    
    #step 3: lookup the user to oauth profile.
    user = request.user
    t_screen_name = access_token['screen_name']
    t_user_id = access_token['user_id']
    t_access_token = access_token['oauth_token']
    t_access_secret = access_token['oauth_token_secret']
    profiles = Profile.objects.get_or_create(user=user, consumer=consumer_obj, oauth_user_id=t_user_id, oauth_screen_name=t_screen_name)
    profile = profiles[0]
    profile.oauth_token = t_access_token
    profile.oauth_secret = t_access_secret
    profile.save()

    url_rd = '/shim/%s'%t_user_id
    return HttpResponseRedirect(url_rd)
    #return HttpResponse()
        
def convert_timeline_json(timeline):
    j = []
    for tl in timeline:
        entitie = tl.entities

def get_oauth_client(profile):
    consumer_token = profile.consumer.token
    consumer_secret = profile.consumer.secret
    access_token = profile.oauth_token
    access_secret = profile.oauth_secret
    consumer = oauth.Consumer(consumer_token, consumer_secret)
    access = oauth.Token(access_token, access_secret)
    client = oauth.Client(consumer, access)
    return client

def user_timeline(request, t_user_id):
    profile = Profile.objects.get(oauth_user_id=t_user_id)
    client = get_oauth_client(profile)
    url_user_timeline = 'http://api.twitter.com/1/statuses/user_timeline.json'
    resp, content = client.request(url_user_timeline, 'GET')
    return HttpResponse(content)
