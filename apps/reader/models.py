from django.db import models

from urlparse import urlparse
import string
from random import Random

class FeedList(models.Model):
    short_url = models.CharField(max_length = 50)
    name      = models.CharField(max_length = 150)

    def get_absolute_url(self):
        return "/view/%s" % self.id

    @staticmethod
    def genToken():
        return "".join(Random().sample(string.letters+string.digits, 6))

class Feed(models.Model):
    title    = models.CharField(max_length = 150)
    feedlist = models.ForeignKey('FeedList')
    url      = models.OneToOneField('Url')

    def __unicode__(self):
        return "<Feed [%s,%s]>" % (self.title, self.url.url)

class Url(models.Model):
    url  = models.URLField(verify_exists=False)
    host = models.ForeignKey('UrlHost')

    def __unicode__(self):
        return "<Url [%s]>" % (self.url[0:50])

    def save(self, *args, **kw):
        if not self.id:
            host = self.find_host()
            urlhost, created = UrlHost.objects.get_or_create(host=host)
            self.host = urlhost
        super(Url, self).save(*args, **kw)

    def find_host(self):
        u = urlparse(self.url)
        return u.netloc

class UrlHost(models.Model):
    host = models.CharField(max_length = 100)

    def __unicode__(self):
        return "<UrlHost [%s]>" % (self.host)
