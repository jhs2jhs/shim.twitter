import urlparse
import oauth2 as oauth


CONSUMER_KEY = 'xoxygrgP3ocua3xnsHHPyA'
CONSUMER_SECRET = 'pHZeJqvBodFVUzlfi24l0ujf22ksdjxiqVmKyT5H7ls'
ACCESS_KEY = '56335495-TyvTUaxO4elqOp2CeFMuOJePem8TgBpgZu3zNUO6o'
ACCESS_SECRET = 'HJYPQIwHCTflsQX0rPkxQP9Bid1cIOSuTvvzCWYwA'

request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'
authorize_url = 'http://twitter.com/oauth/authorize'
saved_searches_url = 'http://api.twitter.com/1/saved_searches.json'
user_timeline_url = 'http://api.twitter.com/1/statuses/user_timeline.json'

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)

token = oauth.Token(ACCESS_KEY, ACCESS_SECRET)
client = oauth.Client(consumer, token)

resp, content = client.request(user_timeline_url, 'GET')
#access_token = dict(urlparse.parse_qsl(content))
#print access_token
print content

'''
print consumer
print client

#get request token
resp, content = client.request(request_token_url, 'GET')
if resp['status'] != '200':
    raise Exception('Invalid response %s.' % resp['status'])
request_token = dict(urlparse.parse_qsl(content))
print request_token

#redirect to provider
path = '%s?oauth_token=%s'%(authorize_url, request_token['oauth_token'])
print path
oauth_verifier = raw_input('pin:')

#once the consumer has redirected the user back to oauth_callback url
#can request the access token the user has approved. 
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, 'POST')
access_token = dict(urlparse.parse_qsl(content))

print access_token
'''
