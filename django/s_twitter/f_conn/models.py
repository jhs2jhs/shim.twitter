from django.db import models

from django.contrib.auth.models import User

class FConsumer(models.Model):
    token = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return unicode(self.add_time)+" : "+self.token

class FOAuth(models.Model):
    user = models.ForeignKey(User, null=False)
    consumer = models.ForeignKey(FConsumer, null=False)
    oauth_user_id = models.CharField(max_length=20, null=True)
    oauth_screen_name = models.CharField(max_length=200, null=True)
    access_token = models.CharField(max_length=200, null=True)
    access_secret = models.CharField(max_length=200, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    save_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.oauth_screen_name+' : '+unicode(self.save_time)
    
    

# Create your models here.
