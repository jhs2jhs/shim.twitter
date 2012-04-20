from my_init import tweepy

print "tweepy is imported"

public_tweets = tweepy.api.public_timeline()
for tweet in public_tweets:
    print tweet.text


import urllib
proxies = urllib.getproxies()
print "proxy setting: %s"%str(proxies)
