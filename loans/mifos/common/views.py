from django.shortcuts import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class AuthorizationRequiredMixin(object):
    """
    Check if authorization key exists
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        ret = None
        if 'auth_key' in request.session:
            ret = super(AuthorizationRequiredMixin,
                            self).dispatch(request, *args, **kwargs)
        else:
            msg = 'not authorized'
            ret = HttpResponse(msg)
        return ret

