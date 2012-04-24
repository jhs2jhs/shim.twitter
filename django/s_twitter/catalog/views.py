# Create your views here.
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
import httplib2
import urllib
import urllib2
import json
from catalog.models import CResource, CRAccess
from django.contrib.auth.decorators import login_required
from datetime import datetime

http = httplib2.Http()
catalog_url = 'http://localhost:8080'
catalog_redirect_url = 'http://localhost:8090/catalog/resource/register/callback'
catalog_resource_access_request_redirect_url = 'http://localhost:8090/catalog/resource/access/callback'
# TODO: check catalog_redirect_url should be same, in practice, it should be different, ask jog why implemented like this
catalog_resource_access_request_redirect_url = catalog_redirect_url 

def hello(request):
    return HttpResponse('hello')

@login_required
def resource_register_request(request):
    # 1.1 resource registration request
    resource_name = 'shim_%s'%(str(datetime.now()))
    params = {
        'resource_name':resource_name,
        'redirect_uri': catalog_redirect_url,
        }
    post_params = urllib.urlencode(params)
    # IMPORTANT: there are two kinds of implementation to send post for resource registeration. one is using httplib2, another one is using urllib2
    # implementation 1: httplib2, headers has to be set as 'content-type=application/x-www.form-urlencoded'. see comments: http://stackoverflow.com/questions/5385699/python-httplib2-http-not-sending-post-parameters
    url = '%s/resource_register'%(catalog_url)
    header = {'content-type':'application/x-www-form-urlencoded'}
    resp, content = http.request(url, 'POST', headers=header, body=urllib.urlencode(params))
    print content
    # implementation 2: urllib2, i get this by reading jog's code: https://github.com/jog/dataware.prefstore/blob/master/src/prefstore/InstallationModule.py
    #req = urllib2.Request(url, post_params)
    #response = urllib2.urlopen(req)
    #print response.read()

    # 1.2 registration success
    result = json.loads(content)
    if not result.has_key('success') :
        raise Exception('1.1 resource registration is not succesful')
    resource_id = result['resource_id']
    print resource_id

    # save accounts into database:
    user = request.user
    resource = CResource.objects.get_or_create(user=user, name=resource_name, registration_id=resource_id)
    resource = resource[0]
    print resource.add_time

    return HttpResponseRedirect('/')

@login_required
def resource_access_request(request, resource_id):
    resource = CResource.objects.get(id=resource_id)
    print resource
    params = {
        'resource_id':resource.registration_id, 
        'redirect_uri':catalog_resource_access_request_redirect_url,
        'state':resource.id,
        }
    params = urllib.urlencode(params)
    url = '%s/resource_request?%s'%(catalog_url, params)
    print url
    #resp, content = http.request(url, 'GET')
    #print content
    # TODO: be careful, the current catalog library with jog does not have correct support for user management in that server, so it would bring some mistake. check to manually add user in mysql first. 
    return HttpResponseRedirect(url)

@login_required
def resource_access_request_callback(request):
    if 'error' in request.REQUEST:
        raise Exception('error return from catalog request authroise')
    #TODO: check state match the correct user id login
    state = request.REQUEST.get('state')
    code = request.REQUEST.get('code')
    resource = CResource.objects.get(id=state)
    access_token = CRAccess.objects.get_or_create(resource=resource, token=code)
    print access_token
    return HttpResponseRedirect('/')
    
    

