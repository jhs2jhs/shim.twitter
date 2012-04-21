# Create your views here.
from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('hello t_conn test')

import tweepy
def test_tweepy(request):
    public_tweets = tweepy.api.public_timeline()
    txt = ''
    for tweet in public_tweets:
        print tweet.text
        txt += tweet.text + '<br>'
    print txt
    return HttpResponse(txt)
        
