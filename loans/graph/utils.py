import json, re
from pymongo import MongoClient

from django.conf import settings
from django.db.models import Q

# graph
from .models import Graph


def normalize_json(j):
    j = j.replace('{u', '{')
    j = j.replace(", u'", ", '")
    j = j.replace(": u'", ": '")
    j = j.replace("{'", '{"')
    j = j.replace("'}", '"}')
    j = j.replace("':", '":')
    j = j.replace("',", '",')
    j = j.replace(": '", ': "')
    j = j.replace(", '", ', "')
    return j


def get_graph_photos(fb_user):
    mongo_client = MongoClient(settings.MONGODB_HOST)
    db = mongo_client.loans
    collection = db.facebook_photos
    photos = collection.find({'user':fb_user.user.id})

    api_type = 'photos'

    for photo in photos:
        obj_id = photo.get('object_id')
        #if not Graph.objects.filter(obj_id=obj_id).count():
        # from
        object_from = photo.get('object_from')
        object_from = normalize_json(object_from)
        try:
            object_from = json.loads(object_from)
        except:
            objects_from = {}
        # tags 
        tags = photo.get('tags')
        tags = normalize_json(tags)
        try:
            tags = json.loads(tags)
        except:
            tags = []
        # likes
        likes = photo.get('likes')
        likes = normalize_json(likes)
        try:
            likes = json.loads(likes)
        except:
            likes = []
        # comments
        #comments = photo.get('comments')
        #comments = normalize_json('comments')
        #try:
        #    comments = json.loads(comments)
        #except:
        #    print comments
        #    comments = []

        try:
            src_uid = object_from.get('id')
            if fb_user.uid in src_uid:
                pass
                #graph.src_uid = fb_user.uid
            else:
                # if action came from different uid
                # check how the user was involve on
                # that post

                # check if src tagged the user
                for tag in tags:
                    if fb_user.uid == tag.get('id'):
                        # check if object action already exist
                        query = Q(obj_id=obj_id)
                        query.add(Q(src_uid=src_uid), Q.AND)
                        query.add(Q(dest_uid=fb_user.uid), Q.AND)
                        query.add(Q(obj_type='tag'), Q.AND)
                        query.add(Q(api_type='photos'), Q.AND)
                        existing_tag = Graph.objects.filter(query).count()
                        if not existing_tag:
                            graph = Graph()
                            graph.obj_id = obj_id
                            graph.src_uid = src_uid
                            graph.dest_uid = fb_user.uid
                            graph.obj_type = 'tag'
                            graph.api_type = 'photos'
                            graph.created_time = photo.get('created_time')
                            graph.save()
                # check if user liked the photo
                for like in likes:
                    if fb_user.uid == like.get('id'):
                        # check if object action already exist
                        query = Q(obj_id=obj_id)
                        query.add(Q(src_uid=fb_user.uid), Q.AND)
                        query.add(Q(dest_uid=src_uid), Q.AND)
                        query.add(Q(obj_type='like'), Q.AND)
                        query.add(Q(api_type='photos'), Q.AND)
                        existing_like = Graph.objects.filter(query).count()
                        if not existing_like:
                            graph = Graph()
                            graph.obj_id = obj_id
                            graph.src_uid = fb_user.uid
                            graph.dest_uid = src_uid
                            graph.obj_type = 'like'
                            graph.api_type = 'photos'
                            graph.created_time = photo.get('created_time')
                            graph.save()
                # check if user commented on the photo
                # note that this will only count as 1
                # even if user has multiple comments
                """
                comment_flag = False
                for comment in comments:
                    # check if already exist
                    query = Q(obj_id=obj_id)
                    query.add(Q(src_uid=fb_user.uid), Q.AND)
                    query.add(Q(dest_uid=src_uid), Q.AND)
                    query.add(Q(obj_type='comment'), Q.AND)
                    query.add(Q(api_type='photos'), Q.AND)
                    existing_comment = Graph.objects.filter(query).count()
                    if existing_comment:
                        comment_flag = True              

                    comment_from = comment.get('from')
                    if fb_user.uid == comment_from.get('id') and not comment_flag:
                        comment_flag = True
                        graph = Graph()
                        graph.obj_id = obj_id
                        graph.src_uid = fb_user.uid
                        graph.dest_uid = src_uid
                        graph.obj_type = 'comment'
                        graph.api_type = 'photos'
                        graph.save()
                """
        except Exception, e:
            print e


def get_graph_posts(fb_user):
    mongo_client = MongoClient(settings.MONGODB_HOST)
    db = mongo_client.loans
    collection = db.facebook_posts
    posts = collection.find({'user':fb_user.user.id})

    api_type = 'posts'

    for post in posts:
        obj_id = post.get('object_id')
        # from
        try:
            object_from = post.get('object_from')
            object_from = normalize_json(object_from)
            object_from = json.loads(object_from)
        except:
            objects_from = {}
        # tags 
        try:
            tags = post.get('with_tags')
            tags = normalize_json(tags)
            with_tags = json.loads(tags)
            tags = with_tags['data']
        except:
            tags = []
        # likes
        try:
            likes = post.get('likes')
            likes = normalize_json(likes)
            likes = json.loads(likes)
        except:
            likes = []

        try:
            src_uid = object_from.get('id')
            if fb_user.uid in src_uid:
                pass
                #graph.src_uid = fb_user.uid
            else:
                # if action came from different uid
                # check how the user was involve on
                # that post

                # check if src tagged the user
                for tag in tags:
                    if fb_user.uid == tag.get('id'):
                        # check if object action already exist
                        query = Q(obj_id=obj_id)
                        query.add(Q(src_uid=src_uid), Q.AND)
                        query.add(Q(dest_uid=fb_user.uid), Q.AND)
                        query.add(Q(obj_type='tag'), Q.AND)
                        query.add(Q(api_type=api_type), Q.AND)
                        existing_tag = Graph.objects.filter(query).count()
                        if not existing_tag:
                            graph = Graph()
                            graph.obj_id = obj_id
                            graph.src_uid = src_uid
                            graph.dest_uid = fb_user.uid
                            graph.obj_type = 'tag'
                            graph.api_type = api_type
                            graph.created_time = post.get('created_time')
                            graph.save()
                # check if user liked the post
                for like in likes:
                    if fb_user.uid == like.get('id'):
                        # check if object action already exist
                        query = Q(obj_id=obj_id)
                        query.add(Q(src_uid=fb_user.uid), Q.AND)
                        query.add(Q(dest_uid=src_uid), Q.AND)
                        query.add(Q(obj_type='like'), Q.AND)
                        query.add(Q(api_type=api_type), Q.AND)
                        existing_like = Graph.objects.filter(query).count()
                        if not existing_like:
                            graph = Graph()
                            graph.obj_id = obj_id
                            graph.src_uid = fb_user.uid
                            graph.dest_uid = src_uid
                            graph.obj_type = 'like'
                            graph.api_type = api_type
                            graph.created_time = post.get('created_time')
                            graph.save()
        except Exception, e:
            print e


def get_graph_videos(fb_user):
    mongo_client = MongoClient(settings.MONGODB_HOST)
    db = mongo_client.loans
    collection = db.facebook_videos
    videos = collection.find({'user':fb_user.user.id})

    api_type = 'videos'

    for video in videos:
        obj_id = video.get('object_id')
        # from
        try:
            object_from = video.get('object_from')
            object_from = normalize_json(object_from)
            object_from = json.loads(object_from)
        except:
            objects_from = {}
        # tags 
        try:
            tags = video.get('tags')
            tags = normalize_json(tags)
            tags = json.loads(tags)
        except:
            tags = []

        try:
            src_uid = object_from.get('id')
            if fb_user.uid in src_uid:
                pass
                #graph.src_uid = fb_user.uid
            else:
                # if action came from different uid
                # check how the user was involve on
                # that video

                # check if src tagged the user
                for tag in tags:
                    if fb_user.uid == tag.get('id'):
                        # check if object action already exist
                        query = Q(obj_id=obj_id)
                        query.add(Q(src_uid=src_uid), Q.AND)
                        query.add(Q(dest_uid=fb_user.uid), Q.AND)
                        query.add(Q(obj_type='tag'), Q.AND)
                        query.add(Q(api_type=api_type), Q.AND)
                        existing_tag = Graph.objects.filter(query).count()
                        if not existing_tag:
                            graph = Graph()
                            graph.obj_id = obj_id
                            graph.src_uid = src_uid
                            graph.dest_uid = fb_user.uid
                            graph.obj_type = 'tag'
                            graph.api_type = api_type
                            graph.created_time = video.get('created_time')
                            graph.save()
        except Exception, e:
            print e


def get_graph_inbox(fb_user):
    mongo_client = MongoClient(settings.MONGODB_HOST)
    db = mongo_client.loans
    collection = db.facebook_inboxes
    inboxes = collection.find({'user':fb_user.user.id})

    api_type = 'inbox'

    for inbox in inboxes:
        try:
            comments = inbox.get('comments')
            comments = normalize_json(comments)
            comments = json.loads(comments)

            profiles = inbox.get('object_to')
            profiles = normalize_json(profiles)
            profiles = json.loads(profiles)
            users =  profiles.get('data')

            for comment in comments:
                query = Q(obj_id=comment.get('id'))
                existing_comment = Graph.objects.filter(query).count()
                if not existing_comment:
                    graph = Graph()
                    graph.obj_id = comment.get('id')
                    # get sender
                    src_uid = comment.get('from')
                    if src_uid is not None:
                        src_uid = src_uid.get('id')
                    graph.src_uid = src_uid
                    # get receiver
                    for user in users:
                        if user.get('id') != src_uid:
                            graph.dest_uid = user.get('id')
                    graph.obj_type = 'conversation'
                    graph.api_type = 'inbox'
                    graph.created_time = comment.get('created_time')
                    graph.save()
        except Exception, e:
            # TODO: do a better json handler
            print e
