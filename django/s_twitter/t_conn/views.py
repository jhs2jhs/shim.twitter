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
from t_conn.models import Profile
import urllib #only use it to encode http url paramater, not use it for http connection

def login_user(request):
    # check whether user is login
    if request.user.is_authenticated():
        print "loginedin already"
        return HttpResponseRedirect('/')
    # if user not login, then manully login
    state = "Please login below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = 'you are successfully logged in!'
                return HttpResponseRedirect('/')
            else:
                state = 'Your account is not active, please register '
        else:
            state = 'Your username and/or password were incorrect.'
    params = {'state':state, 'username':username, 'password':password}
    return render_to_response('auth.html', params, context_instance=RequestContext(request))

@login_required()
def twitter_list(request):
    if request.user.is_authenticated():
        print "yes"
    else:
        print "no"
    #views.login(request)
    c = RequestContext(request)
    return render_to_response('base.html', c)

consumer = oauth.Consumer(settings.TWITTER_CONSUMER_TOKEN, settings.TWITTER_CONSUMER_SECRET)
client = oauth.Client(consumer)
#print settings.twitter_request_token_url
oauth_callback = urllib.urlencode({'oauth_callback':'http://localhost:8080/login/authenticated/'})

def twitter_login(request):
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

def twitter_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def twitter_authenticated(request):
    #step 1: use the request token in the session to build a new client. 
    print request.session['request_token']
    token = oauth.Token(request.session['request_token']['oauth_token'], request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    
    #step 2: request the authorized access token from Twitter
    resp, content = client.request(settings.TWITTER_ACCESS_TOKEN_URL, 'GET')
    if resp['status'] != '200':
        raise Exception ('Invalid response from twitter')
    access_token = dict(cgi.parse_qsl(content))
    print access_token
    
    #step 3: lookup the user or create them if they donot exist.
    try:
        user = User.objects.get(username = access_token['screen_name'])
        print user
    except User.DoesNotExist:
        user = User.objects.create_user(access_token['screen_name'], '%s@twitter.com'%access_token['screen_name'], '1234')
        profile = Profile()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()
    user = authenticate(username=access_token['screen_name'], password=access_token['screen_name'])
    print user
    login(request, user)

    #return HttpResponseRedirect('/')
    return HttpResponse()


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
