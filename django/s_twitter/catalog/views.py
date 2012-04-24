# Create your views here.
from django.shortcuts import HttpResponse
import httplib2
import urllib
import urllib2

http = httplib2.Http()
catalog_url = 'http://localhost:8080'
catalog_redirect_url = 'http://localhost:8090/catalog/resource/request_callback'

def hello(request):
    return HttpResponse('hello')

def resource_request(request):
    params = {
        'resource_name':'shim',
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
    req = urllib2.Request(url, post_params)
    response = urllib2.urlopen(req)
    print response.read()
    return HttpResponse('world')

