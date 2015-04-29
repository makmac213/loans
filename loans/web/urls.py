from django.conf.urls import patterns, include, url

# web
from .views import FrontendView, FacebookView, OdeskView

urlpatterns = patterns('',
    # landing page
    url(r'^$', FrontendView.Landing.as_view(), name="landing"),
    # questions page
    url(r'^questions/$', FrontendView.Questions.as_view(), name="questions"),
    # ajax check graph task
    url(r'^check-graph-task/$', 
            FrontendView.CheckGraphTask.as_view(),
            name="check_graph_task"),

    # Facebook
    url(r'^new-association-redirect-url/$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^new-association-redirect-url/#_=_$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^logged-in/$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^logged-in/#_=_$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^new-users-redirect-url/$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),
    url(r'^new-users-redirect-url/#_=_$', 
            FacebookView.NewAssociation.as_view(), name="fb_new_association"),

    # odesk
    url(r'^odesk/$', 
            OdeskView.LinkAccount.as_view(), 
            name="odesk_landing"),
    url(r'^odesk/redirect/$', 
            OdeskView.Redirect.as_view(), 
            name="odesk_redirect"),

)
