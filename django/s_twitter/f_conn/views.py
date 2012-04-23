# Create your views her
from django.shortcuts import HttpResponse, render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import Template, RequestContext
from django.core.context_processors import csrf
import json
from f_conn.models import FConsumer, FOAuth
import httplib2
import urllib
import urlparse

def get_consumer():
    token = settings.FACEBOOK_CONSUMER_TOKEN
    secret = settings.FACEBOOK_CONSUMER_SECRET
    consumer_objs = FConsumer.objects.get_or_create(token=token, secret=secret)
    #consumer_oauth = oauth.
    return consumer_objs[0]

FACEBOOK_OAUTH_URL = 'https://www.facebook.com/dialog/oauth'
FACEBOOK_REDIRECT_URL_INIT = 'http://localhost:8080/oauth/facebook/init'
FACEBOOK_REDIRECT_URL_REQUEST = 'http://localhost:8080/oauth/facebook/request'
FACEBOOK_REDIRECT_URL_AUTHENTICATED = 'http://localhost:8080/oauth/facebook/authenticated'
FACEBOOK_ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
FACEBOOK_OAUTH_SCOPE = 'user_photo_video_tags,friends_photo_video_tags'

client = httplib2.Http()

@login_required
def facebook_oauth_init(request):
    # step 0: have the state param ready, it is stored in session as refered later by facebook redirect
    user = request.user
    state = request.session['facebook_oauth_state_user_in_django'] = user.id

    # step 1: redirect the user to the oauth dialog
    url_params = {
        'client_id':settings.FACEBOOK_CONSUMER_TOKEN,
        'redirect_uri':FACEBOOK_REDIRECT_URL_REQUEST,
        'scope':FACEBOOK_OAUTH_SCOPE, 
        'state':str(state)
        }
    url = '%s?%s'%(FACEBOOK_OAUTH_URL, urllib.urlencode(url_params))
    #print url
    
    # step 2: the user is prompted to authorize applicaiton
    return HttpResponseRedirect(url)


def facebook_oauth_request(request):
    # step 3: the user is redirected back to app
    # check if user decliend
    if 'error_reason' in request.REQUEST:
        error_reason = request.REQUEST.get('error_reason')
        error = request.REQUEST.get('error')
        error_description = request.REQUEST.get('error_description')
        return HttpResponse('%s <br>%s <br>%s <br>'%(error_reason, error, error_description))
    # is user accept
    state = request.REQUEST.get('state')
    code = request.REQUEST.get('code')
    # check if the user is the right user
    if str(state) != str(request.user.id):
        logout(request)
        return HttpResponseRedirect('/')
    
    # step 4: exchange the code for a user access token
    url_params = {
        'client_id': settings.FACEBOOK_CONSUMER_TOKEN,
        # TODO: it look like the redirect_url should be same here to in step 1. I have to add other code in step 1 to check whether it redirected-redirected or just redirect
        'redirect_uri': FACEBOOK_REDIRECT_URL_REQUEST, #AUTHENTICATED, 
        'client_secret': settings.FACEBOOK_CONSUMER_SECRET,
        'code': code,
        }
    url = '%s?%s'%(FACEBOOK_ACCESS_TOKEN_URL, urllib.urlencode(url_params))
    #print url
    #print code
    resp, content = client.request(url, 'GET')
    #print resp, content
    #if resp['status'] != '400':
    #    raise Exception('Return 400, error in authentication')
    if resp['status'] != '200':
        raise Exception('Return %s in step 4: invalid response from facebook'%(resp['status']))
    response_token = urlparse.parse_qs(content)
    access_token = response_token['access_token'][0]
    expire_token = response_token['expires'][0]
    
    # step 5: make requests to the graph api
    facebook_me_url = 'https://graph.facebook.com/me'
    params = {'access_token':access_token}
    url = '%s?%s'%(facebook_me_url, urllib.urlencode(params))
    resp, content = client.request(url, 'GET')
    if resp['status'] != '200':
        raise Exception('Return %s in step 5: invalid response from facebook'%(resp['status']))
    
    # finish the oauth to save the tokens. 
    user = request.user
    consumer_obj = get_consumer()
    fme = json.loads(content)
    f_screen_name = fme['username']
    f_user_id = fme['id']
    foauth = FOAuth.objects.get_or_create(user=user, consumer=consumer_obj, oauth_user_id=f_user_id, oauth_screen_name=f_screen_name)
    foauth = foauth[0]
    foauth.access_token = access_token
    foauth.save()
    #TODO: facebook oauth expired variable does not set here. 

    return HttpResponse(content)

# TODO need to delete this method
def facebook_oauth_authenticated(request):
    # step 3: the user is redirected back to app
    # check if user decliend
    if 'error_reason' in request.REQUEST:
        error_reason = request.REQUEST.get('error_reason')
        error = request.REQUEST.get('error')
        error_description = request.REQUEST.get('error_description')
        return HttpResponse('%s <br>%s <br>%s <br>'%(error_reason, error, error_description))
    # is user accept
    state = request.REQUEST.get('state')
    code = request.REQUEST.get('code')
    
    # step 4: exchange the code for a user access token
    url_params = {
        'client_id': settings.FACEBOOK_CONSUMER_TOKEN,
        'redirect_uri': state
        }
    return HttpResponse('hello')

@login_required
def user_photo_tagged(request, f_user_id):
    foauth = FOAuth.objects.get(oauth_user_id=f_user_id)
    f_access_token = foauth.access_token
    # api can be evaluate here: http://developers.facebook.com/tools/explorer/?method=GET&path=me%2Fphotos
    facebook_me_photos_url = 'https://graph.facebook.com/me/photos'
    params = {'access_token':f_access_token}
    url = '%s?%s'%(facebook_me_photos_url, urllib.urlencode(params))
    resp, content = client.request(url, 'GET')
    if resp['status'] != '200':
        raise Exception('Return %s in step 5: invalid response from facebook'%(resp['status']))
    return HttpResponse(content)
