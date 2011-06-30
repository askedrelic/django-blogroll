from django.contrib import admin
from apps.reader.models import *

admin.site.register(FeedList)
admin.site.register(Feed)
admin.site.register(Url)
admin.site.register(UrlHost)
