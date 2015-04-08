import requests, logging, urllib3
from pymongo import MongoClient

from django.conf import settings
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.utils.html import strip_tags

# djcelery
from celery import task

# facebook
from .models import Like, Photo, Video

urllib3.disable_warnings()

logger = logging.getLogger(__name__)

FB_ME = settings.FB_ME

@task
def scrape_likes(fb_user):
    """
    Get and save all of user's liked items
    """

    url = '%slikes?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        # while data has next page follow next pages
        # need to use has_next flag because of no do..while loop
        # in python
        has_next = True
        while has_next:
            likes_json = r.json()
            for like_json in likes_json.get('data'):
                # NOTE: using pymongo to query an existing collections
                # unable to use MongoDBManager's filter.
                # Check if object has been previously saved
                mongo_client = MongoClient(settings.MONGODB_HOST)
                db = mongo_client.loans
                collection = db.facebook_likes
                existing = collection.find_one({'object_id': like_json.get('id')})
                # if not existing, get and save current object
                if existing is None:
                    like = Like()
                    like.user = fb_user.user.id
                    like.category = like_json.get('category')
                    like.created_time = like_json.get('created_time')
                    like.object_name = like_json.get('name')
                    like.object_id = like_json.get('id')
                    like.raw = like_json
                    like.save()
            # check if current request has next page
            # if none mark has_next flag as false
            paging = likes_json.get('paging')
            if paging is not None:
                paging_next = paging.get('next')
                if paging_next is not None:
                    r = requests.get(paging_next)
                    if r.status_code != 200:
                        has_next = False
                else:
                    has_next = False
            else:
                has_next = False


def get_object_list(objects_json):
    """
    Gets all data
    """
    tags = []
    # check that the json passed is not none
    if objects_json is not None:
        has_next = True
    else:
        has_next = False

    while has_next:
        for object_json in objects_json.get('data'):
            tags.append(object_json)
        # check if current request has next page
        # if none mark has_next flag as false
        paging = objects_json.get('paging')
        if paging is not None:
            paging_next = paging.get('next')
            if paging_next is not None:
                r = requests.get(paging_next)
                if r.status_code == 200:
                    objects_json = r.json()
                else:
                    has_next = False
            else:
                has_next = False
        else:
            has_next = False
    return tags


@task
def scrape_photos(fb_user):
    """
    Get and save all of user's liked photos
    """
    url = '%sphotos?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        # while data has next page follow next pages
        # need to use has_next flag because of no do..while loop
        # in python
        has_next = True
        while has_next:
            photos_json = r.json()
            for photo_json in photos_json.get('data'):
                # NOTE: using pymongo to query an existing collections
                # unable to use MongoDBManager's filter.
                # Check if object has been previously saved
                mongo_client = MongoClient(settings.MONGODB_HOST)
                db = mongo_client.loans
                collection = db.facebook_photos
                existing = collection.find_one({'object_id': photo_json.get('id')})
                # if not existing, get and save current object
                if existing is None:
                    # TODO: programmatically loop thru keys
                    photo = Photo()
                    photo.user = fb_user.user.id
                    photo.object_id = photo_json.get('id')
                    photo.album = photo_json.get('album')
                    photo.backdated_time = photo_json.get('backdated_time')
                    photo.backdated_time_granularity = photo_json.get('backdated_time_granularity')
                    photo.created_time = photo_json.get('created_time')
                    photo.event = photo_json.get('event')
                    photo.object_from = photo_json.get('from')
                    photo.height = photo_json.get('height')
                    photo.icon = photo_json.get('icon')
                    photo.images = photo_json.get('images')
                    photo.link = photo_json.get('link')
                    photo.name = photo_json.get('name')
                    photo.picture = photo_json.get('picture')
                    photo.place = photo_json.get('place')
                    photo.source = photo_json.get('source')
                    photo.updated_time = photo_json.get('updated_time')
                    photo.width = photo_json.get('width')
                    # get tags
                    photo.tags = get_object_list(photo_json.get('tags'))
                    # get likes
                    photo.likes = get_object_list(photo_json.get('likes'))
                    # get comments
                    photo.comments = get_object_list(photo_json.get('comments'))
                    photo.raw = photo_json
                    photo.save()
            # check if current request has next page
            # if none mark has_next flag as false
            paging = photos_json.get('paging')
            if paging is not None:
                paging_next = paging.get('next')
                if paging_next is not None:
                    r = requests.get(paging_next)
                    if r.status_code != 200:
                        has_next = False
                else:
                    has_next = False
            else:
                has_next = False


@task
def scrape_videos(fb_user):
    """
    Get and save all of user's liked photos
    """
    url = '%svideos?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        # while data has next page follow next pages
        # need to use has_next flag because of no do..while loop
        # in python
        has_next = True
        while has_next:
            videos_json = r.json()
            for video_json in videos_json.get('data'):
                # NOTE: using pymongo to query an existing collections
                # unable to use MongoDBManager's filter.
                # Check if object has been previously saved
                mongo_client = MongoClient(settings.MONGODB_HOST)
                db = mongo_client.loans
                collection = db.facebook_videos
                existing = collection.find_one({'object_id': video_json.get('id')})
                # if not existing, get and save current object
                if existing is None:
                    # TODO: programmatically loop thru keys
                    video = Video()
                    video.user = fb_user.user.id
                    video.object_id = video_json.get('id')
                    video.created_time = video_json.get('created_time')
                    video.description = video_json.get('description')
                    video.embed_html = video_json.get('embed_html')
                    video.format = video_json.get('format')
                    video.object_from = video_json.get('from')
                    video.icon = video_json.get('icon')
                    video.icon = video_json.get('length')
                    video.name = video_json.get('name')
                    video.picture = video_json.get('picture')
                    video.source = video_json.get('source')
                    video.updated_time = video_json.get('updated_time')
                    # get tags
                    video.tags = get_object_list(video_json.get('tags'))
                    # get comments
                    video.comments = get_object_list(video_json.get('comments'))
                    video.raw = video_json
                    video.save()
            # check if current request has next page
            # if none mark has_next flag as false
            paging = videos_json.get('paging')
            if paging is not None:
                paging_next = paging.get('next')
                if paging_next is not None:
                    r = requests.get(paging_next)
                    if r.status_code != 200:
                        has_next = False
                else:
                    has_next = False
            else:
                has_next = False
