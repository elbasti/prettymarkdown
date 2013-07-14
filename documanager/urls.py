from django.conf.urls import patterns, include, url

urlpatterns = patterns('documanager.views',
        url(r'^$', 'index', name='index'),
)


