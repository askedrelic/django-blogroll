# -*- coding: UTF-8 -*-

from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings

import json
import string
from random import Random

from apps.reader.models import Feed as rssFeed, Url, UrlHost, FeedList

from libgreader import Feed, GoogleReader, OAuthMethod

def startAuth(request):
    if request.method == 'POST':
        #start oauth request
        my_token  = settings.OAUTH_KEY
        my_secret = settings.OAUTH_SECRET
        auth = OAuthMethod(my_token, my_secret)

        callback  = settings.SERVER_HOST +  "share/"
        auth.setCallback(callback)

        token, token_secret = auth.setAndGetRequestToken()
        print token, token_secret
        request.session[token] = token_secret
        print auth.buildAuthUrl()
        return HttpResponseRedirect(auth.buildAuthUrl())
    else:
        return HttpResponse(500)

def share(request):
    my_token  = settings.OAUTH_KEY
    my_secret = settings.OAUTH_SECRET
    auth = OAuthMethod(my_token, my_secret)

    if request.method == 'POST':
        feed_title = request.POST.getlist('feed_title[]')
        feed_url = request.POST.getlist('feed_url[]')
        if len(feed_url) and len(feed_title) == len(feed_url):
            db_feedlist = FeedList.objects.create(name='test_new')
            for i in xrange(0,len(feed_url)):
                title = feed_title[i]
                url   = feed_url[i]
                #@TODO better error checking against urls
                newUrl = Url.objects.create(url=url)
                newFeed = rssFeed.objects.create(url=newUrl, title=title[0:150], feedlist=db_feedlist)

        return redirect(db_feedlist)
    elif request.GET.get('oauth_verifier', False) and request.GET.get('oauth_token', False):
        #try getting the token key and secret from session

        # NOTE: can get into state where session can't be found? or token can't
        # be found? try waiting?
        # import IPython; IPython.embed()
        token    = request.GET['oauth_token']
        secret   = request.session[token]
        verifier = request.GET['oauth_verifier']
        auth.setAccessTokenFromCallback(token, secret, verifier)
        googleFeedList = getGoogleFeeds(auth)

        #feedList = createFeeds(googleFeedList)
        feedList = list()
        for feed in googleFeedList:
            if feed.feedUrl is not None:
                feedList.append((feed.title, feed.feedUrl))
        #request.session['user_feed_list'] = feedList
        #request.session['user_feed_list'] = user_feed_list
        return direct_to_template(request, 'reader/share.html', locals())
    else:
        return direct_to_template(request, 'reader/share.html', locals())
        # return HttpResponse(500)

def createFeeds(feedList = list()):
    db_feedlist, created = FeedList.objects.get_or_create(name='test')
    userList = list()
    for feed in feedList:
        if feed.feedUrl:
            newUrl = Url(url=feed.url)
            host = newUrl.find_host()
            if host:
                uh, created = UrlHost.objects.get_or_create(host=host)
                newUrl.host = uh
                newUrl.save()

            #from IPython.Shell import IPShellEmbed; shell = IPShellEmbed(); shell();
            newFeed = rssFeed(url=newUrl, title=feed.title[0:150], feedlist=db_feedlist)
            newFeed.save()
            userList.append(newFeed)
    return userList

def view(request, id):
    """
    View a feedlist
    """
    user_feed_list = FeedList.objects.get(pk=id)
    user_feed_list = user_feed_list.feed_set.all()

    if user_feed_list:
        templateLocation = 'reader/view.html'
        return direct_to_template(request, templateLocation, locals())
    else:
        return HttpResponse(500)

def getGoogleFeeds(auth):
    try:
        google = GoogleReader(auth)
    except IOError:
        #handle username/password error
        #redirect to homepage with error?
        pass

    if google.buildSubscriptionList():
        return google.getFeeds()
