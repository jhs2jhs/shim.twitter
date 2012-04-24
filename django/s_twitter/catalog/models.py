from django.db import models
from django.contrib.auth.models import User

#TODO: catalog, resource, processor should all be in different class. now they are in same just for testing. 


class CResource(models.Model):
    user = models.ForeignKey(User, null=False)
    name = models.CharField(max_length=128)
    registration_id = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)
    save_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name

class CRAccess(models.Model):
    resource = models.ForeignKey(CResource)
    token = models.CharField(max_length=200, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    save_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.resource.name+"**"+self.token


# Create your models here.
