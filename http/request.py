

from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import AnonymousUser
from io import StringIO

import json

class FakeRequest:
    def __init__(self):
        """
            @description: Il s'agit ici d'une classe destiner à simuler un fausse requêtes.
        """
        
    def is_authenticated(self):
        """_summary_
        """
        return True
    
def generate_fake_request(path='/', user=None):
    """
        @description: Il s'agit ici de générer une fausse requête.
    """
    request = WSGIRequest({
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': path,
        'wsgi.input': StringIO()
    })
    request.user = AnonymousUser() if user is None else user
    return request

def RequestPost(request):
    """
        @description: Il s'agit ici de récupérer la varibles POST et de la renvoyer.
    """
    if len(request.body) == 0:
        return request.POST
    try:
        return json.loads(request.body)
    except:
        return request.POST
