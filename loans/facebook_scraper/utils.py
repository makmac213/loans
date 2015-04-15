import requests, json
from pymongo import MongoClient

from django.conf import settings

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
