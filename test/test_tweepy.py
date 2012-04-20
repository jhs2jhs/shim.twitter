from my_init import tweepy

print "tweepy is imported"

public_tweets = tweepy.api.public_timeline()
for tweet in public_tweets:
    print tweet.text

print "\n\n\n"

import urllib
proxies = urllib.getproxies()
print "proxy setting: %s"%str(proxies)

CONSUMER_KEY = 'xoxygrgP3ocua3xnsHHPyA'
CONSUMER_SECRET = 'pHZeJqvBodFVUzlfi24l0ujf22ksdjxiqVmKyT5H7ls'
'''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
import webbrowser
webbrowser.open(auth_url)
print 'please authorize:'+auth_url
verifier = raw_input('PIN:').strip()
auth.get_access_token(verifier)
print 'ACCESS_KEY = "%s"'%auth.access_token.key
print 'ACCESS_SECRET = "%s"'%auth.access_token.secret
'''


ACCESS_KEY = '56335495-TyvTUaxO4elqOp2CeFMuOJePem8TgBpgZu3zNUO6o'
ACCESS_SECRET = 'HJYPQIwHCTflsQX0rPkxQP9Bid1cIOSuTvvzCWYwA'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
#import sys
#api.update_status(sys.argv[1])
#user = api.get_user('twitter')
#print user
#print user.screen_name
#print user.followers_count
#for friend in user.friends():
#    print friend.screen_name
print api.public_timeline()[1]
print len(api.public_timeline())
#print api.get_status()
user = api.get_user('JianhuaShao')
me = api.me()
print me.screen_name
print me.followers_count
print api.rate_limit_status()
print api.saved_searches()
#print api.trends()
#print api.list_members()

def get_status(api, uid, max_id):
    if max_id == None:
        tl = api.user_timeline(user_id=uid)
    else:
        tl = api.user_timeline(user_id=uid, max_id=max_id)
    print tl
    print '\n\n==='
    for status in tl:
        print status.id, status.text
        max_id = status.id
    return max_id

uid = 62496976
max_id = get_status(api, uid, max_id=None)
while True:
    max_id = get_status(api, uid, max_id)
    print max_id
    #check if max_id is same or not








