from django.conf.urls import patterns, include, url

# web
from .views import FrontendView, FacebookView

urlpatterns = patterns('',
    # landing page
    url(r'^$', FrontendView.Landing.as_view(), name="landing"),
    # questions page
    url(r'^questions/$', FrontendView.Questions.as_view(), name="questions"),


    # Facebook
    url(r'^new-association-redirect-url/$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^new-association-redirect-url/#_=_$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^logged-in/$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^logged-in/#_=_$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
)
