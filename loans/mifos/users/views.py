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

# mifos.common
from mifos.common.utils import build_url
from mifos.common.views import AuthorizationRequiredMixin

logger = logging.getLogger(__name__)


class AuthView(object):

    class Authenticate(View):
        """
        https://demo.openmf.org/api-docs/apiLive.htm#authenticate_request
        """
        api = 'authentication'

        def post(self, request, *args, **kwargs):
            username = settings.MIFOS_USERNAME
            password = settings.MIFOS_PASSWORD
            request_url = build_url(self.api, username=username, 
                                        password=password)
            response = request.post(request_url)

            ret = 'not authorized'
            if response.status_code == '200':
                data = response.json()
                request.session['auth_key'] = data.get('base64EncodedAuthenticationKey')
                ret = 'authorized'

            return HttpResponse(ret)                

        @method_decorator(csrf_exempt)
        def dispatch(self, *args, **kwargs):
            return super(AuthView.Authenticate,
                            self).dispatch(*args, **kwargs)


class UserView(object):
    """
    https://demo.openmf.org/api-docs/apiLive.htm#users
    """

    class List(AuthorizationRequiredMixin, View):
        api = 'users'

        def get(self, request, *args, **kwargs):
            auth_key = "Basic %s" % request.session.get('auth_key')
            headers = {
                'Authorization': auth_key
                'X-Mifos-Platform-TenantId': settings.MIFOS_TENANT_ID
            }
            request_url = build_url(self.api)
            response = request.post(request_url, headers=headers)
            ret = response.json()
            return HttpResponse(ret)


    class User(AuthorizationRequiredMixin, View):
        api = 'users'

        def get(self, request, *args, **kwargs):
            """
            retrieve a user
            """ 
            ret = None
            user_id = kwargs.get('user_id')
            if user_id is not None:
                auth_key = "Basic %s" % request.session.get('auth_key')
                headers = {
                    'Authorization': auth_key,
                    'Content-type': 'application/json',
                    'X-Mifos-Platform-TenantId': settings.MIFOS_TENANT_ID,
                }
                request_url = build_url('%s/%s' % (self.api, user_id))
                response = request.get(request_url, headers=headers)
                ret = response.json()
            else:
                ret = 'invalid request'
            return HttpResponse(ret)

        def post(self, request, *args, **kwargs):
            """
            create a user
            """
            ret = None
            auth_key = "Basic %s" % request.session.get('auth_key')
            headers = {
                'Authorization': auth_key
                'X-Mifos-Platform-TenantId': settings.MIFOS_TENANT_ID
            }
            request_url = build_url(self.api)
            response = request.post(request_url, headers=headers)
            ret = response.json()

            return HttpResponse(ret)
