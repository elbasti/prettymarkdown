from django.conf.urls import patterns, include, url

urlpatterns = patterns('documanager.views',
        url(r'^$', 'index', name='index'),
        url(r'^email_pdf$', 'email_pdf', name='email_pdf'),
        url(r'^sent$', 'sent_confirm', name='sent')
)


