# Create your views here.
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
        
def convert_timeline_json(timeline):
    j = []
    for tl in timeline:
        entitie = tl.entities
