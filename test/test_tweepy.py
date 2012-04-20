from my_init import tweepy

print "tweepy is imported"

public_tweets = tweepy.api.public_timeline()
for tweet in public_tweets:
    print tweet.text
