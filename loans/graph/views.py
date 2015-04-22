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
from django.db.models import Count, Q
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

# graph
from .models import Graph

class GraphView(object):

    class UserGraph(View):
        template_name = 'graph/user_graph.html'

        def get(self, request, *args, **kwargs):
            date_range = request.GET.get('date_range')
            start_date = ''
            end_date = ''
            if date_range is not None and date_range != '':
                tmp = date_range.split(' to ')
                start_date = datetime.strptime(tmp[0], "%Y-%m-%d")
                end_date = datetime.strptime(tmp[1], "%Y-%m-%d")
            # get social auth user
            social_user = request.user.social_auth.get(provider='facebook')
            # get inbox
            query_inbox = Q(src_uid=social_user.uid)
            if date_range is not None and date_range != '':
                query_inbox.add(Q(created_time__gte=start_date), Q.AND)
                query_inbox.add(Q(created_time__lte=end_date), Q.AND)
            # sent
            messages_sent = Graph.objects.filter(query_inbox).values(
                                'dest_uid').annotate(
                                    dcount=Count('dest_uid')).order_by('-dcount')[:10]
            print messages_sent.query.__str__()
            messages_sent_count = Graph.objects.filter(
                                    src_uid=social_user.uid).count()
            # received
            messages_received = Graph.objects.filter(query_inbox).values(
                                    'src_uid').annotate(
                                        dcount=Count('src_uid')).order_by('-dcount')[:10]
            print messages_received.query.__str__()
            messages_received_count = Graph.objects.filter(
                                    dest_uid=social_user.uid).count()

            context = {
                'page_title': 'User Graph Activity',
                'messages_sent': messages_sent,
                'messages_sent_count': messages_sent_count,
                'messages_received': messages_received,
                'messages_received_count': messages_received_count,
                'start_date': start_date,
                'end_date': end_date,
            }
            return render(request, self.template_name, context)
