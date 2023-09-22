
from django.contrib.auth.models import User
from kernel.http import Response
import json
import urllib

def load_json(function):
    """Charge le profile à l'intérieurs des éléments."""
    def wrap(request, *args, **kwargs):
        try: 
            request.POST = json.loads(request.body.decode('utf-8'))
        except:
            pass
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap