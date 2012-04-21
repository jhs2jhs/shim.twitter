# Create your views here.
from django.shortcuts import HttpResponse, render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import oauth2 as oauth
import myutil
import cgi
from t_conn.models import Profile


consumer = oauth.Consumer(settings.TWITTER_CONSUMER_TOKEN, settings.TWITTER_CONSUMER_SECRET)
client = oauth.Client(consumer)
#print settings.twitter_request_token_url

def twitter_login(request):
    #step 1: get a request token from twitter
    resp, content = client.request(settings.TWITTER_REQUEST_TOKEN_URL, 'GET')
    if resp['status'] != '200':
        raise Exception('Invalid response from Twitter')

    #step 2: store the request token in a session for later use
    request.session['request_token'] = dict(cgi.parse_qsl(content))
    print request.session['request_token']

    #step 3: redirect the user to the authenticate URL. 
    #url = '%s?oauth_token=%s'%(settings.TWITTER_AUTHENTICATE_URL, request.session['request_token']['oauth_token'])
    url = '%s?oauth_token=%s'%(settings.TWITTER_AUTHORIZE_URL, request.session['request_token']['oauth_token'])
    print url

    return HttpResponseRedirect(url)

def twitter_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def twitter_authenticated(request):
    #step 1: use the request token in the session to build a new client. 
    token = oauth.Token(request.session['request_token']['oauth_token'], request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    
    #step 2: request the authorized access token from Twitter
    resp, content = client.request(access_token_url, 'GET')
    if resp['status'] != '200':
        print content
        raise Exception ('Invalid response from twitter')
    access_token = dict(cgi.parse_qsl(content))
    
    #step 3: lookup the user or create them if they donot exist.
    try:
        user = User.objects.get(username = access_token['screen_name'])
    except User.DoesNotExist:
        user = User.objects.create_user(access_token['screen_name'], '%s@twitter.com'%access_token['screen_name'], access_token['oauth_token_secret'])
        profile = Profile()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()
    user = authenticate(username=access_token['screen_name'], password=access_token['oauth_token_secret'])
    login(request, user)

    return HttpResponseRedirect('/')


'''
def twitter_connect(request):
    consumer = auth.Consumer(myutil.CONSUMER_KEY, myutil.CONSUMER_SECRET)
    try:
        next = '/dashboard/'
        # cheking for a 'redirect' in request.session, if have already stroed your twitter credentials in the database then it will redirect you to the dashboard, else you will follow the regular twitter authentication protocol. 
        if ('redirect' in request.session):
            next = request.session['redirect']
            del request.session['redirect']
        # should i check whether user login or not?
        twitter = Client_Twitter.objects.get(user=request.user.get_profile())
        return HttpResponseRedirect(next)
'''
        
def convert_timeline_json(timeline):
    j = []
    for tl in timeline:
        entitie = tl.entities
