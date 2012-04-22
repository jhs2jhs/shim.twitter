from django.db import models
from django.contrib.auth.models import User

class Consumer(models.Model):
    token = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return unicode(self.add_time)+" : "+self.token

class Profile(models.Model):
    user = models.ForeignKey(User, null=False)
    consumer = models.ForeignKey(Consumer, null=False)
    oauth_user_id = models.CharField(max_length=20, null=True)
    oauth_screen_name = models.CharField(max_length=200, null=True)
    oauth_token = models.CharField(max_length=200, null=True)
    oauth_secret = models.CharField(max_length=200, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.oauth_screen_name+" : "+unicode(self.modify_time)

