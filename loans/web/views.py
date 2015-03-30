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
from django.utils import timezone, translation
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic import (FormView, TemplateView, DetailView, 
                                    ListView, UpdateView)

logger = logging.getLogger(__name__)

class FrontendView(object):

    class Landing(TemplateView):
        template_name = 'web/index.html'

        def get(self, request, *args, **kwargs):
            user = request.user.social_auth.filter(provider="facebook")[0]
            friends = None
            if user:
                # friends list
                # TODO: move graph url to settings
                
                url = 'https://graph.facebook.com/%s/' % (user.uid)
                url += 'friends?fields=id,name,location,picture'
                url += '&access_token=%s' % (user.extra_data.get('access_token'))
                print url
                """
                url = 'https://graph.facebook.com/v2.3/me/friends?' \
                        'access_token=%s' % (user.extra_data.get('access_token'))
                """

                r = requests.get(url)

                if r.status_code == 200:                    
                    friends = r.json()              

            context = {
                'user':user,
                'friends':friends,
            }
            return render(request, self.template_name, context)

    #class Info


class FacebookView(View):

    class NewAssociation(View):

        def get(self, request, *args, **kwargs):
            social_user = request.user.social_auth.filter(provider="facebook")[0]

            photos = None
            if social_user:
                # photo list
                # TODO: move graph url to settings
                url = 'https://graph.facebook.com/v2.3/me/'
                url += 'photos/?access_token=%s' % (social_user.access_token)

                r = requests.get(url)

                if r.status_code == 200:                    
                    photos = r.json()
                logger.info(photos)

            return HttpResponse('get')