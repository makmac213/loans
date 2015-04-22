import requests, logging, urllib3
from pymongo import MongoClient

from django.conf import settings
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.utils.html import strip_tags

# djcelery
from celery import task

# graph
from graph.models import GraphTask

# facebook
from .models import Feed, Like, Photo, Video, Post, Inbox

urllib3.disable_warnings()

logger = logging.getLogger(__name__)

FB_ME = settings.FB_ME

@task
def scrape_likes(fb_user, session_id):
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
    # task completed flag graph task
    try:
        graph_task = GraphTask.objects.get(user=fb_user.user, 
                                        session_id=session_id)
        graph_task.task_likes = True 
        graph_task.save()   
    except GraphTask.DoesNotExist, e:
        print e


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
def scrape_inbox(fb_user, session_id):
    """
    Get all conversations
    """
    url = '%sinbox?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        has_next = True
        while has_next:
            conversations = r.json()
            for conversation in conversations.get('data'):
                mongo_client = MongoClient(settings.MONGODB_HOST)
                db = mongo_client.loans
                collection = db.facebook_inboxes
                existing = collection.find_one({'object_id': conversation.get('id')})
                if existing is None:
                    inbox = Inbox()
                    inbox.user = fb_user.user.id
                    inbox.object_id = conversation.get('id')
                    # get comments
                    inbox.comments = get_object_list(conversation.get('comments'))
                    inbox.object_to = conversation.get('to')
                    inbox.unread = conversation.get('unread')
                    inbox.unseen = conversation.get('unseen')
                    inbox.updated_time = conversation.get('updated_time')
                    inbox.save()
            # check if current request has next page
            # if none mark has_next flag as false
            paging = conversations.get('paging')
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
    # task completed flag graph task
    try:
        graph_task = GraphTask.objects.get(user=fb_user.user, 
                                        session_id=session_id)
        graph_task.task_inbox = True 
        graph_task.save()   
    except GraphTask.DoesNotExist, e:
        print e


@task
def scrape_photos(fb_user, session_id):
    """
    Get and save all of user's photos
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
                    #photo.backdated_time = photo_json.get('backdated_time')
                    #photo.backdated_time_granularity = photo_json.get('backdated_time_granularity')
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
    # task completed flag graph task
    try:
        graph_task = GraphTask.objects.get(user=fb_user.user, 
                                        session_id=session_id)
        graph_task.task_photos = True  
        graph_task.save()  
    except GraphTask.DoesNotExist, e:
        print e


@task
def scrape_videos(fb_user, session_id):
    """
    Get and save all of user's videos
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
    # task completed flag graph task
    try:
        graph_task = GraphTask.objects.get(user=fb_user.user, 
                                        session_id=session_id)
        graph_task.task_videos = True
        graph_task.save()    
    except GraphTask.DoesNotExist, e:
        print e


@task
def scrape_feeds(fb_user, session_id):
    """
    Get and save all of user's feeds
    """
    url = '%sfeed?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        # while data has next page follow next pages
        # need to use has_next flag because of no do..while loop
        # in python
        has_next = True
        while has_next:
            feeds_json = r.json()
            for feed_json in feeds_json.get('data'):
                # NOTE: using pymongo to query an existing collections
                # unable to use MongoDBManager's filter.
                # Check if object has been previously saved
                mongo_client = MongoClient(settings.MONGODB_HOST)
                db = mongo_client.loans
                collection = db.facebook_feeds
                existing = collection.find_one({'object_id': feed_json.get('id')})
                # if not existing, get and save current object
                if existing is None:
                    # TODO: programmatically loop thru keys
                    feed = Feed()
                    feed.user = fb_user.user.id
                    feed.object_id = feed_json.get('id')
                    feed.object_from = feed_json.get('from')
                    feed.object_to = feed_json.get('to')
                    feed.with_tags = feed_json.get('with_tags')
                    feed.message = feed_json.get('message')
                    feed.story = feed_json.get('story')
                    feed.story_tags = feed_json.get('story_tags')
                    feed.picture = feed_json.get('picture')
                    feed.link = feed_json.get('link')
                    feed.icon = feed_json.get('icon')
                    feed.privacy = feed_json.get('privacy')
                    feed.object_type = feed_json.get('type')
                    feed.feed_id = feed_json.get('object_id')
                    feed.created_time = feed_json.get('created_time')
                    feed.updated_time = feed_json.get('updated_time')
                    feed.is_hidden = feed_json.get('is_hidden')
                    feed.subscribed = feed_json.get('subscribed')

                    # get likes
                    feed.likes = get_object_list(feed_json.get('likes'))
                    # get comments
                    feed.comments = get_object_list(feed_json.get('comments'))
                    feed.raw = feed_json
                    feed.save()
            # check if current request has next page
            # if none mark has_next flag as false
            paging = feeds_json.get('paging')
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
    # task completed flag graph task
    try:
        graph_task = GraphTask.objects.get(user=fb_user.user, 
                                        session_id=session_id)
        graph_task.task_feeds = True  
        graph_task.save()  
    except GraphTask.DoesNotExist, e:
        print e


@task
def scrape_posts(fb_user, session_id):
    """
    Get and save all of user's posts
    """
    url = '%sfeed?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        # while data has next page follow next pages
        # need to use has_next flag because of no do..while loop
        # in python
        has_next = True
        while has_next:
            posts_json = r.json()
            for post_json in posts_json.get('data'):
                # NOTE: using pymongo to query an existing collections
                # unable to use MongoDBManager's filter.
                # Check if object has been previously saved
                mongo_client = MongoClient(settings.MONGODB_HOST)
                db = mongo_client.loans
                collection = db.facebook_feeds
                existing = collection.find_one({'object_id': post_json.get('id')})
                # if not existing, get and save current object
                if existing is None:
                    # TODO: programmatically loop thru keys
                    post = Post()
                    post.user = fb_user.user.id
                    post.object_id = post_json.get('id')
                    post.object_from = post_json.get('from')
                    post.object_to = post_json.get('to')
                    post.with_tags = post_json.get('with_tags')
                    post.message = post_json.get('message')
                    post.story = post_json.get('story')
                    post.story_tags = post_json.get('story_tags')
                    post.picture = post_json.get('picture')
                    post.link = post_json.get('link')
                    post.icon = post_json.get('icon')
                    post.privacy = post_json.get('privacy')
                    post.object_type = post_json.get('type')
                    post.post_id = post_json.get('object_id')
                    post.created_time = post_json.get('created_time')
                    post.updated_time = post_json.get('updated_time')
                    post.is_hidden = post_json.get('is_hidden')
                    post.subscribed = post_json.get('subscribed')
                    post.status_type = post_json.get('status_type')
                    post.name = post_json.get('name')
                    post.caption = post_json.get('caption')
                    post.description = post_json.get('description')

                    # get likes
                    post.likes = get_object_list(post_json.get('likes'))
                    # get comments
                    post.comments = get_object_list(post_json.get('comments'))

                    post.raw = post_json
                    post.save()
            # check if current request has next page
            # if none mark has_next flag as false
            paging = posts_json.get('paging')
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
    # task completed flag graph task
    try:
        graph_task = GraphTask.objects.get(user=fb_user.user, 
                                        session_id=session_id)
        graph_task.task_posts = True
        graph_task.save()    
    except GraphTask.DoesNotExist, e:
        print e


@task
def extend_access_token(fb_user):
    url = 'https://graph.facebook.com/oauth/access_token?' \
            'client_id=%s&client_secret=%s&grant_type=fb_exchange_token&' \
            'fb_exchange_token=%s'  % (settings.SOCIAL_AUTH_FACEBOOK_KEY, 
                                        settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                                        fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.text
        data = data.split('&')
        extra_data = fb_user.extra_data
        access_token = extra_data.get('access_token')
        expires = extra_data.get('expires')
        for tmp in data:
            kv = tmp.split('=')
            if kv[0] == 'access_token':
                access_token = kv[1]
            elif kv[0] == 'expires':
                expires = kv[1]
        extra_data['access_token'] = access_token
        extra_data['expires'] = expires
        fb_user.extra_data = extra_data
        fb_user.save()
        logger.info('Access token extended')