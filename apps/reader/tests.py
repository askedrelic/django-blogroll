"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from apps.reader.views import *
from apps.reader.models import Feed as rssFeed, Url, UrlHost

class mockFeed(object):
    def __init__(self, siteUrl, title):
        self.siteUrl = siteUrl
        self.title = title

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class TestFeed(TestCase):
    def setUp(self):
        self.feedlist = [mockFeed("http://www.gogole.com", "googl"), mockFeed("http://www.shacknews.com", 'shack')]

    def test_create_new_feedlist(self):
        fl = create_new_feedlist(self.feedlist)
        u = Url.objects.get(pk=1)
        self.assertEqual(u.url, self.feedlist[0].siteUrl)
