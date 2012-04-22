from django.db import models
from django.contrib.auth.models import User

class Consumer(models.Model):
    token = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    add_time = models.DateField(auto_now_add=False)

class Profile(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)
    def __unicode__(self):
        return self.user.user.username

# Create your models here.
class Client_Twitter(models.Model):
    #user = models.OneToOneField('Client') 
    twitter_id = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    access_token = models.CharField(max_length=200, null=True)
    access_token_secret = models.CharField(max_length=200, null=True)
    twitter_username = models.CharField(max_length=200, null=True)
    # how to link the twitter account to user account in this applicaiton , and also in the catalog in the furture. 
    def __unicode__(self):
        #return self.user.user.username
        return self.twitter_username
