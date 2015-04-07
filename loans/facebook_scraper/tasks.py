import requests, logging, urllib3
from pymongo import MongoClient

from django.conf import settings
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.utils.html import strip_tags

# djcelery
from celery import task

# facebook
from .models import Like

urllib3.disable_warnings()

logger = logging.getLogger(__name__)

FB_ME = settings.FB_ME

@task
def scrape_likes(fb_user):
    url = '%slikes?access_token=%s' % (FB_ME, fb_user.access_token)
    r = requests.get(url)
    if r.status_code == 200:
        has_next = True
        likes = []
        while has_next:
            likes_json = r.json()
            for like_json in likes_json.get('data'):
                mongo_client = MongoClient('mongodb://localhost:27017/')
                db = mongo_client.loans
                collection = db.facebook_likes
                existing = collection.find_one({'object_id': like_json.get('id')})
                if existing is None:
                    like = Like()
                    like.user = fb_user.user.id
                    like.category = like_json.get('category')
                    like.created_time = like_json.get('created_time')
                    like.object_name = like_json.get('name')
                    like.object_id = like_json.get('id')
                    like.raw = like_json
                    like.save()
                    logger.info(like)
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