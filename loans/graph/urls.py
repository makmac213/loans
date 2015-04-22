from django.conf.urls import patterns, include, url

# web
from .views import GraphView

urlpatterns = patterns('',
    # graph
    url(r'^graph/users/(?P<user_id>\d+)/$', 
            GraphView.UserGraph.as_view(), 
            name="users_graph"),
    
)
