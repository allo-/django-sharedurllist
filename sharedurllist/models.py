from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    class Meta:
        unique_together = ("user", "name")
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Token(models.Model):
    user = models.ForeignKey(User)
    device = models.ForeignKey(Device)
    token = models.CharField(max_length=36, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.token


class Url(models.Model):
    user = models.ForeignKey(User)
    device = models.ForeignKey(Device)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return self.content
