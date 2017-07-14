from django.conf.urls import url
from .views import *
from django.views.generic.base import TemplateView

app_name='hiring'
urlpatterns = [
    url(r'^$',home,name='home'),
    url(r'^signup/$',signup,name='signup'),
    url(r'^login/$',userlogin,name='login'),
    url(r'^emailsent/$',  TemplateView.as_view(template_name="emailsent.html"), name="emailsent"),
    url(r'^event(?P<pk>[0-9]+)/calender/$',  calenderview, name="calender"),
    url(r'^afterverification/(?P<token>.*)/$', afterverify, name="afterverification"),
    url(r'^logout/$',userlogout,name='logout'),
    url(r'^events/$',showevents,name='events'),
    url(r'^event(?P<pk>[0-9]+)/$',showevent,name='event'),
    url(r'^register/(?P<events_id>[0-9]+)/(?P<key>[0-9]+)/(?P<start_date>[^/]+)/(?P<start_time>[^/]+)/$',register,name = 'register'),
    url(r'^agree/(?P<pk>[0-9]+)/$',agree,name='agree'),
    url(r'^test/(?P<pk>[0-9]+)/$',test,name='test'),
    url(r'^question/(?P<pk>[0-9]+)/$',question,name='question'),
    url(r'^solution/(?P<pk>[0-9]+)/(?P<testpk>[0-9]+)/$',solution,name='solution'),
    url(r'^save/(?P<pk>[0-9]+)/(?P<testpk>[0-9]+)/$',next,name='save'),

]
