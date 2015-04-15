from django.conf.urls import patterns, include, url

# web
from .views import MongoAdminView, UserView

urlpatterns = patterns('',
	# mongodb views
    url(r'^collections/(?P<collection_name>.*)/$', 
            MongoAdminView.ManageCollection.as_view(), 
            name="manage_collection"),
    url(r'^collections/$', 
            MongoAdminView.ListCollection.as_view(), 
            name="list_collections"),
    url(r'^documents/(?P<collection>\w+)/(?P<object_id>.*)/$', 
            MongoAdminView.ViewDocument.as_view(), 
            name="view_document"),

    # users
    url(r'^users/(?P<pk>\d+)/$', 
            UserView.Detail.as_view(), 
            name="user_detail"),
    url(r'^users/$', 
            UserView.ListUsers.as_view(), 
            name="list_users"),

)
