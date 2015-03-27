from django.conf.urls import patterns, include, url

# web
from .views import FrontendView

urlpatterns = patterns('',
    url(r'^$', FrontendView.Landing.as_view(), name="landing"),
)
