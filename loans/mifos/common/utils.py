from urllib import urlencode

from django.conf import settings

def build_url(api, **kwargs):
    api_url = settings.MIFOS_API_URL
    url = '%s%s' % (api_url, api)
    if len(kwargs):
        url += '?%s' % (urlencode(kwargs))
    return url