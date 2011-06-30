from django.conf.urls.defaults import patterns

urlpatterns = patterns('reader.views',
    (r'^redirect/$', 'startAuth'),
    (r'^share/$', 'share'),
    (r'^view/([0-9]+)$', 'view'),
    #(r'^v/([a-zA-Z0-9]*)$', 'view'),
    #(r'^v/([a-zA-Z0-9]{10})$', 'view'),
)
