import httplib2
import urllib
import json

access_token = 'M/0QCguqCX/G4qRTQyyAjZyT8nCTCTTwUFEm27AhIIg='

resource_url = 'http://localhost:8090/catalog/resource/access/test'
params = {
    'access_token':access_token
    }
post_params = urllib.urlencode(params)
url = '%s?%s'%(resource_url, post_params)
http = httplib2.Http()
resp, content = http.request(url, 'GET')
"==========output=========="
#print content
"==========output=========="

content = json.loads(content)
twitter = content['twitter']
facebook = content['facebook']
print '==========twitter==========='
print twitter
print '==========twitter==========='
print '==========facebook==========='
print facebook
print '==========facebook==========='

