from django.conf.urls import patterns, include, url

urlpatterns = patterns('documanager.views',
        url(r'^$', 'index', name='index'),
        url(r'^browser$', 'print_to_browser', name='print_to_browser'),
)


