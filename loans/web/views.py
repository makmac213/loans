import json, time, os, string, requests, logging
import odesk
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
                                    scrape_feeds, scrape_posts, scrape_inbox,
                                    scrape_albums, extend_access_token)

# graph
from graph.models import GraphTask

# odesk scraper
from odesk_scraper.models import OdeskProfile, Engagement

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
                # create graph tasks
                try:
                    graph_task = GraphTask.objects.get(
                                    session_id=request.session.session_key)
                except GraphTask.DoesNotExist:
                    graph_task = GraphTask()
                    graph_task.user = request.user
                    graph_task.session_id = request.session.session_key
                    graph_task.save()
                    # start tasks
                    scrape_likes.delay(social_user, graph_task.session_id)
                    scrape_photos.delay(social_user, graph_task.session_id)
                    scrape_videos.delay(social_user, graph_task.session_id)
                    scrape_feeds.delay(social_user, graph_task.session_id)
                    scrape_posts.delay(social_user, graph_task.session_id)
                    scrape_inbox.delay(social_user, graph_task.session_id)
                    # just update facebook friend count on profile
                    scrape_friends_count.delay(social_user)
                    #scrape_albums.delay(social_user, graph_task.session_id)
                    # extend token
                    extend_access_token.delay(social_user)
                except Exception, e:
                    # multiple results
                    print e
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


    class CheckGraphTask(View):
        def post(self, request, *args, **kwargs):
            try:
                graph_task = GraphTask.objects.get(
                                session_id=request.session.session_key)
                is_completed = graph_task.is_completed
            except GraphTask.DoesNotExist:
                is_completed = False
            context = {
                'is_completed': is_completed,
            }
            return HttpResponse(json.dumps(context))

        @method_decorator(csrf_exempt)
        def dispatch(self, *args, **kwargs):
            return super(FrontendView.CheckGraphTask,
                            self).dispatch(*args, **kwargs)


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


class OdeskView(View):

    class LinkAccount(View):

        def get(self, request, *args, **kwargs):
            client = odesk.Client(settings.ODESK_API_KEY,
                                    settings.ODESK_API_SECRET)
            url = client.auth.get_authorize_url()
            request.session['request_token'] = client.auth.request_token
            request.session['request_token_secret'] = client.auth.request_token_secret
            return redirect(url)


    class Redirect(View):
        def get(self, request, *args, **kwargs):
            oauth_token = request.GET.get('oauth_token')
            oauth_verifier = request.GET.get('oauth_verifier')
            client = odesk.Client(settings.ODESK_API_KEY, 
                                    settings.ODESK_API_SECRET)
            client.auth.key = settings.ODESK_API_KEY
            client.auth.secret = settings.ODESK_API_SECRET
            client.auth.request_token = request.session.get('request_token')
            client.auth.request_token_secret = request.session.get('request_token_secret')

            token, secret = client.auth.get_access_token(oauth_verifier)
            client = odesk.Client(settings.ODESK_API_KEY, 
                                    settings.ODESK_API_SECRET,
                                    oauth_access_token=token,
                                    oauth_access_token_secret=secret)
            info = client.hr.get_user_me()
            auth_json = client.auth.get_info()
            auth_info = auth_json.get('info')
            capacity = auth_info.get('capacity')
            location = auth_info.get('location')

            engagements_json = client.hr.get_engagements()
            engagements = engagements_json.get('engagement')

            # update odesk profile
            try:
                profile = OdeskProfile.objects.get(user=request.user)
            except OdeskProfile.DoesNotExist:
                profile = OdeskProfile()
            profile.user = request.user
            profile.reference = info.get('reference')
            profile.odesk_id = info.get('id')
            profile.first_name = info.get('first_name')
            profile.last_name = info.get('last_name')
            profile.timezone = info.get('timezone')
            profile.timezone_offset = info.get('timezone_offset')
            profile.is_provider = info.get('is_provider')
            profile.status = info.get('status')
            # auth info
            profile.portrait_50_img = auth_info.get('portrait_50_img')
            profile.portrait_32_img = auth_info.get('portrait_32_img')
            profile.portrait_100_img = auth_info.get('portrait_100_img')
            profile.ref = auth_info.get('ref')
            profile.has_agency = int(auth_info.get('has_agency', 0))
            profile.company_url = auth_info.get('company_url')
            profile.capacity_provider = capacity.get('provider')
            profile.capacity_buyer = capacity.get('buyer')
            profile.capacity_affiliate_manager = capacity.get('affiliate_manager') 
            profile.city = location.get('city')
            profile.state = location.get('state')
            profile.country = location.get('country')
            profile.profile_url = auth_info.get('profile_url')
            profile.save()

            # engagements
            for engagement in engagements:
                existing_query = Q(profile=profile)
                existing_query.add(Q(reference=engagement.get('reference')), Q.AND)
                if not Engagement.objects.filter(existing_query).count():
                    eng = Engagement()
                    eng.profile = profile
                    eng.buyer_team_id = engagement.get('buyer_team__id')
                    eng.buyer_team_reference = engagement.get('buyer_team__reference')
                    eng.created_time = engagement.get('created_time')
                    eng.description = engagement.get('description')
                    eng.dev_recno_ciphertext = engagement.get('dev_recno_ciphertext')
                    eng.engagement_end_date = engagement.get('engagement_end_date')
                    eng.engagement_job_type = engagement.get('engagement_job_type')
                    eng.engagement_start_date = engagement.get('engagement_start_date')
                    eng.engagement_title = engagement.get('engagement_title')
                    eng.hourly_charge_rate = engagement.get('hourly_charge_rate')
                    eng.hourly_pay_rate = engagement.get('hourly_pay_rate')
                    is_paused = engagement.get('is_paused', 0)
                    if is_paused != '':
                        eng.is_paused = int(is_paused)
                    eng.is_trial_assignment = engagement.get('is_trial_assignment')
                    eng.job_title = engagement.get('job__title')
                    eng.job_ref_ciphertext = engagement.get('job_ref_ciphertext')
                    eng.offer_reference = engagement.get('offer__reference')
                    eng.portrait_url = engagement.get('portrait_url')
                    eng.provider_id = engagement.get('provider__id')
                    eng.provider_reference = engagement.get('provider__reference')
                    eng.provider_team_id = engagement.get('provider_team__id')
                    eng.provider_team_reference = engagement.get('provider_team__reference')
                    eng.reference = engagement.get('reference')
                    eng.status = engagement.get('status')
                    eng.weekly_hours_limit = engagement.get('weekly_hours_limit')
                    eng.weekly_salary_charge_amount = engagement.get('weekly_salary_charge_amount')
                    eng.weekly_salary_pay_amount = engagement.get('weekly_salary_pay_amount')
                    # get users total earnings per engagement                                        
                    provider_ref = eng.provider_reference
                    # get epoch date to datetime
                    date_format = '%Y-%m-%d'
                    start_date = float(eng.engagement_start_date) / 1000.0
                    start_date = datetime.fromtimestamp(
                                    start_date).strftime(date_format)
                    end_date = float(eng.engagement_end_date) / 1000.0
                    end_date = datetime.fromtimestamp(
                                    end_date).strftime(date_format)
                    # only get the total sum for the company based from the
                    # date range, default to 0 if none was found
                    query = "SELECT SUM(amount) WHERE date >= '%s' " \
                            "AND date <= '%s' AND buyer_team__reference = %s" \
                            % (start_date, end_date, eng.buyer_team_reference)
                    earnings_json = client.finreport.get_provider_earnings(provider_ref, query)
                    earnings_table = earnings_json.get('table')
                    try:
                        total_earnings = earnings_table['rows'][0]['c'][0]['v']
                    except:
                        total_earnings = 0
                    eng.total_earnings = total_earnings
                    eng.save()

            return HttpResponse(json.dumps(earnings_json))