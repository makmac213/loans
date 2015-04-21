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

# answers
from answers.models import Answer

# facebook_scraper
from facebook_scraper.tasks import (scrape_likes, scrape_photos, scrape_videos,
                                    scrape_feeds, scrape_posts, 
                                    extend_access_token)

# questions
from questions.models import Question

logger = logging.getLogger(__name__)

class FrontendView(object):

    class Landing(TemplateView):
        template_name = 'web/index.html'

        def get(self, request, *args, **kwargs):
            try:
                user = request.user.social_auth.filter(provider="facebook")[0]
            except:
                user = None
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

    
    class Questions(View):
        template_name = 'web/questions.html'

        def get(self, request, *args, **kwargs):
            questions = Question.objects.filter(is_active=True, 
                                                is_deleted=False)
            try:
                social_user = request.user.social_auth.filter(
                                                    provider="facebook")[0]
                scrape_likes.delay(social_user)
                scrape_photos.delay(social_user)
                scrape_videos.delay(social_user)
                scrape_feeds.delay(social_user)
                scrape_posts.delay(social_user)
                # extend token
                extend_access_token.delay(social_user)
            except:
                social_user = None
            context = {
                'questions': questions,
            }
            return render(request, self.template_name, context)

        def post(self, request, *args, **kwargs):
            my_answers = Answer()

            # infos
            # https://github.com/selwin/django-user_agents
            infos = {
                'is_mobile': request.user_agent.is_mobile,
                'is_tablet': request.user_agent.is_tablet,
                'is_touch_capable': request.user_agent.is_touch_capable,
                'is_pc': request.user_agent.is_pc,
                'is_bot': request.user_agent.is_bot,
                'browser': request.user_agent.browser.family,
                'browser_version': request.user_agent.browser.version_string,
                'os': request.user_agent.os.family,
                'os_version': request.user_agent.os.version_string,
                'device': request.user_agent.device,
            }

            # location
            infos['latitude'] = request.POST.get('latitude')
            infos['longitude'] = request.POST.get('longitude')

            # screensize
            infos['screensize'] = request.POST.get('screensize')
            # flash version
            infos['flash_version'] = request.POST.get('flash')
            # cookies enabled
            infos['cookies_enabled'] = request.POST.get('cookies')
            # timezone
            infos['timezone'] = request.POST.get('timezone')
            # connection
            infos['connection'] = request.POST.get('connection')
            # display
            infos['display'] = request.POST.get('display')
            # font smoothing
            infos['font_smoothing'] = request.POST.get('fontsmoothing')
            # fonts
            infos['fonts'] = request.POST.get('fonts')
            # java
            infos['java'] = request.POST.get('java')
            # language
            infos['language'] = request.POST.get('language')
            # latency
            infos['latency'] = request.POST.get('latency')
            # silverlight
            infos['silverlight'] = request.POST.get('silverlight')
            # true browser
            infos['true_browser'] = request.POST.get('true_browser')
            # user agent
            infos['user_agent'] = request.POST.get('user_agent')
            # plugins
            infos['plugins'] = request.POST.get('plugins')
            
            infos_json = json.dumps(infos)
            logger.info(infos_json)
            my_answers.infos = infos_json

            # get uid
            try:
                social_user = request.user.social_auth.filter(
                                                    provider="facebook")[0]
                my_answers.uid = social_user.uid
            except:
                social_user = None

            # get answers
            answers = []
            for k, v in request.POST.iteritems():
                if 'qid' in k:
                    answer = {}
                    qid = k.split('-')[1]
                    question = Question.objects.get(id=int(qid))
                    answer['question_id'] = qid
                    answer['answer'] = v
                    answer['question_text'] = question.text
                    answers.append(answer)

            for k, v in request.FILES.iteritems():
                logger.info(k)
                logger.info(v)
                answer = {}
                qid = k.split('-')[1]
                question = Question.objects.get(id=int(qid))
                answer['question_id'] = qid
                answer['answer'] = v.name
                answer['question_text'] = question.text

                file_path = os.path.join(settings.MEDIA_ROOT, 
                                            'question_uploads')
                tmp_name = os.urandom(8).encode('hex')
                try:
                    ext = v.name.split('.')[-1]
                except:
                    ext = ''
                full_path = '%s/%s.%s' % (file_path, tmp_name, ext)
                with open(full_path, 'wb+') as dest:
                    for chunk in v.chunks():
                        dest.write(chunk)
                answer['sys_file_path'] = full_path
                answers.append(answer)

            answers_json = json.dumps(answers)
            my_answers.content = answers_json

            my_answers.save()
            logger.info(answers_json)

            questions = Question.objects.filter(is_active=True, 
                                                is_deleted=False)
            context = {
                'questions': questions,
            }
            return render(request, self.template_name, context)


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

            return redirect('questions')