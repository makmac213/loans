import requests, json, warnings
from pymongo import MongoClient
from datetime import datetime, timedelta, date

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
# graph
from graph.models import Graph

# fb me graph url
FB_ME = settings.FB_ME

def get_profile_picture(uid):
    ret = None
    url = '%s%s/picture?redirect=false' % (settings.FB_GRAPH_URL, uid)
    r = requests.get(url)
    if r.status_code == 200:
        ret = r.json()
    return ret


def get_likes(user_id):
    client = MongoClient(settings.MONGODB_HOST)
    db = client.loans
    collection = db.facebook_likes
    likes = collection.find({'user':user_id})
    return likes


def get_photos(user_id):
    client = MongoClient(settings.MONGODB_HOST)
    db = client.loans
    collection = db.facebook_photos
    photos = collection.find({'user':user_id})
    return photos

def get_photos_places(user_id):
    client = MongoClient(settings.MONGODB_HOST)
    db = client.loans
    collection = db.facebook_photos
    query = {
        'user': user_id,
        'place': {'$ne': None}
    }
    photos = collection.find(query)
    places_json = []
    for photo in photos:
        latitude = photo['place']
        latitude = latitude.replace('{u', '{')
        latitude = latitude.replace(", u'", ", '")
        latitude = latitude.replace(": u'", ": '")
        latitude = json.loads(latitude)
        latitude = latitude
        longitude = latitude
        #name = latitude['name']
        place = {
            'lat': str('%s' % latitude),
            'lng': str('%s' % longitude),
        }
        places_json.append(place)
    return places_json


def get_videos(user_id):
    client = MongoClient(settings.MONGODB_HOST)
    db = client.loans
    collection = db.facebook_videos
    videos = collection.find({'user':user_id})
    return videos


def get_feeds(user_id):
    client = MongoClient(settings.MONGODB_HOST)
    db = client.loans
    collection = db.facebook_feeds
    feeds = collection.find({'user':user_id})
    return feeds

def get_facebook_incoming_count(user, interval=None):
    """
    user = User object
    interval = interval in days from current date
    """

    # suppress warning for comparing naive & aware dates
    warnings.filterwarnings("ignore")
    # TODO: properly catch exceptions here
    fb_user = user.social_auth.get(provider='facebook')
    dest_uid = fb_user.uid
    # build query
    query = Q(dest_uid=dest_uid)
    if interval is not None and isinstance(interval, int):
        end_date = date.today()
        start_date = end_date - timedelta(days=interval)
        query.add(Q(created_time__gte=start_date), Q.AND)
        query.add(Q(created_time__lte=end_date), Q.AND)        

    graph = Graph.objects.filter(query).count()
    return graph

def get_facebook_outgoing_count(user, interval=None):
    """
    user = User object
    interval = interval in days from current date
    """
    # suppress warning for comparing naive & aware dates
    warnings.filterwarnings("ignore")
    # TODO: properly catch exceptions here
    fb_user = user.social_auth.get(provider='facebook')
    src_uid = fb_user.uid
    # build query
    query = Q(src_uid=src_uid)
    if interval is not None and isinstance(interval, int):
        end_date = date.today()
        start_date = end_date - timedelta(days=interval)
        query.add(Q(created_time__gte=start_date), Q.AND)
        query.add(Q(created_time__lte=end_date), Q.AND)       

    graph = Graph.objects.filter(query).count()
    return graph


def get_friends_count(user):
    """
    user = User object
    returns updated total friends count.
    fallback to profile friends count if
    in case fb graph api is not available.
    also updates friends count in profile. 
    """
    # suppress warnings
    warnings.filterwarnings("ignore")
    profile = user.get_profile()
    total_count = profile.friends_count
    fb_user = user.social_auth.get(provider='facebook')
    url = '%sfriends?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        total_count = r.json()['summary']['total_count']
        # update total count on profile
        if total_count != profile.friends_count:
            profile.friends_count = total_count
    return total_count