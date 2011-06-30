from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'index.views.index'),

    (r'', include('apps.reader.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

#DEBUG Let django host static content during development.
import settings
if settings.development.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.development.MEDIA_ROOT}),
    )
