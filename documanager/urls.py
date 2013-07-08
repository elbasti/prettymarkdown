from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^$', 'documanager.views.index', name='index'),
)

