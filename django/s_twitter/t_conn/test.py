from django.shortcuts import HttpResponse
import json

def hello(request):
    return HttpResponse('hello t_conn test')

import tweepy
def test_tweepy(request):
    public_tweets = tweepy.api.public_timeline()
    txt = ''
    for tweet in public_tweets:
        #print json.dumps(tweet)
        txt += tweet.text + '<br>'
    #print txt
    print tweepy.api.__getattribute__
    print '\n'
    print dir(public_tweets[0])
    return HttpResponse(txt)

import urlparse
import oauth2 as oauth
def test_oauth2(request):
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
    print content
    return HttpResponse(content)
