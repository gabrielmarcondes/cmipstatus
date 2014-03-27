from django.conf.urls.defaults import patterns, include, url
from views import Home, ExpList, ExpView, IncludeNewExp, ExcludeExp
from views import MemberView
from views import AlertView, AlertDismiss, Filecheck
#from models import FeedFetcher

urlpatterns = patterns('',
    url(r'^$', Home.as_view()),
    url(r'^list/$', ExpList.as_view()),
    url(r'^expview/(?P<expid>\d+)/$', ExpView.as_view()),
    url(r'^member/(?P<memberid>\d+)/$', MemberView.as_view()),
    url(r'^include/$', IncludeNewExp.as_view()),
    url(r'^exclude/$', ExcludeExp.as_view()),
    url(r'^alert/view/(?P<alertid>\d+)/$', AlertView.as_view()),
    url(r'^alert/dismiss/(?P<alertid>\d+)/$', AlertDismiss.as_view()),
    url(r'^filecheck/$', Filecheck.as_view()),
#    url(r'^news/$', 'cmipstatus.views.newslist'),
#    url(r'^news/feed/$', FeedFetcher()),
#    url(r'^validation/(\w{3}\d{3})(_\d+)?/$', 'cmipstatus.views.expvalview'),
#    url(r'^outputs/$', 'cmipstatus.views.outputsview'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'gmaologin.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/exps/login/'}),
    )
