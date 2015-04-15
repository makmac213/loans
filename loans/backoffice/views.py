import json, time, os, string, requests, logging
from datetime import datetime, timedelta
from copy import deepcopy
from decimal import Decimal
from time import mktime

# django
from django import forms
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sessions.backends.db import Session
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.loading import get_model
from django.http import HttpResponseRedirect, QueryDict, HttpResponseForbidden
from django.shortcuts import (HttpResponse, redirect, render_to_response, 
                                get_object_or_404, render)
from django.template import RequestContext, Context, Template
from django.template.defaultfilters import floatformat
from django.template.loader import render_to_string
from django.utils import timezone, translation, simplejson
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic import (FormView, TemplateView, DetailView, 
                                    ListView, UpdateView)

# facebook_scraper
from facebook_scraper.utils import (get_profile_picture, get_likes,
                                    get_photos, get_videos, get_photos_places)
from facebook_scraper.models import Feed, Like, Photo, Video, Post

# pymongo
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class MongoAdminView(object):

    class ListCollection(View):
        template_name = 'backoffice/list_collections.html'

        def get(self, request, *args, **kwargs):
            client = MongoClient(settings.MONGODB_HOST)
            non_rel = settings.DB_NONREL
            db = getattr(client, settings.DATABASES[non_rel]['NAME'])
            collections = db.collection_names()

            context = {
                'collections': collections,
            }
            return render(request, self.template_name, context)


    class ManageCollection(View):
        template_name = 'backoffice/manage_collection.html'

        def get(self, request, *args, **kwargs):
            skip = request.GET.get('skip', 0)
            limit = request.GET.get('limit', 10)
            date_range = request.GET.get('date_range')

            collection_name = kwargs.get('collection_name')
            client = MongoClient(settings.MONGODB_HOST)
            non_rel = settings.DB_NONREL
            db = getattr(client, settings.DATABASES[non_rel]['NAME'])
            collection = getattr(db, collection_name)
            query = {}
            if date_range is not None and date_range != '':
                tmp = date_range.split(' to ')
                start_date = datetime.strptime(tmp[0], "%Y-%m-%d")
                end_date = datetime.strptime(tmp[1], "%Y-%m-%d")
                query = {'created_time':{'$gte':start_date, '$lte':end_date}}
            docs = collection.find(query).skip(int(skip)).limit(int(limit))

            context = {
                'collection_name': collection_name,
                'docs': docs,
                'skip': skip,
                'limit': limit,
                'date_range': date_range,
            }
            return render(request, self.template_name, context)


    class ViewDocument(View):
        template_name = 'backoffice/view_document.html'

        def get(self, request, *args, **kwargs):
            collection = kwargs.get('collection')
            object_id = kwargs.get('object_id')
            client = MongoClient(settings.MONGODB_HOST)
            non_rel = settings.DB_NONREL
            db = getattr(client, settings.DATABASES[non_rel]['NAME'])
            col = getattr(db, collection)
            data = col.find_one({'object_id':object_id})
            context = {
                'collection': collection,
                'data': data,
            }
            return render(request, self.template_name, context)


class UserView(object):

    class ListUsers(ListView):
        model = User
        template_name = 'backoffice/users/list.html'
        queryset = User.objects.filter(is_superuser=False)


    class Detail(DetailView):
        model = User
        template_name = 'backoffice/users/detail.html'

        def get_context_data(self, **kwargs):
            context = super(UserView.Detail, self).get_context_data(**kwargs)
            user = context['object']
            social_user = user.social_auth.get(provider='facebook')
            profile_pic = get_profile_picture(social_user.uid)
            if profile_pic is not None:
                if not profile_pic['data']['is_silhouette']:
                    context['profile_pic'] = profile_pic['data']['url']
            # significant other
            significant_other = user.profile.significant_other
            if significant_other is not None:
                significant_other = significant_other.replace('{u', '{')
                significant_other = significant_other.replace(", u'", ", '")
                significant_other = significant_other.replace(": u'", ": '")
                significant_other = json.loads('"%s"' % significant_other)
                context['significant_other'] = significant_other
            # work
            work = user.profile.work
            work = work.replace('{u', '{')
            work = work.replace(", u'", ", '")
            work = work.replace(": u'", ": '")
            work = json.loads('"%s"' % work)
            context['work'] = work
            # likes
            context['likes'] = get_likes(user.id)
            # photos
            context['photos'] = get_photos(user.id)
            context['places'] = get_photos_places(user.id)
            # videos
            context['videos'] = get_videos(user.id)
            return context




