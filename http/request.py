

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
    
def generate_fake_request(path='/', user=None, profile=None):
    """
        @description: Il s'agit ici de générer une fausse requête.
        @params.path: Il s'agit ici du chemin de la requête.
        @params.user: Il s'agit ici de l'utilisateur de la requête.
    """
    if profile is not None:
        user = profile.user
        
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

def httpGetKey(request, key):
    """
        @description: Get POST value, if not found, get QueryParams value.
    """
    value = request.POST.get(key, '>>NOTFOUND<<')
    if value != '>>NOTFOUND<<':
        return request.GET.get(key)
    return value