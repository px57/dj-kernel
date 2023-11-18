from django.core.exceptions import PermissionDenied
import json
from kernel.websocket.base import websocket__readqueryparams
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from profiles.models import Profile

def websocket__simplifier(function):
    """Charge le profile a l'interieurs des elements. 
    re

    Args:
        request.page_profile): Ajoute le profile chargee just ici
    """
    def fakeConnect(scope):
        """
            @description: 
        """
        if settings.DEBUG is False: 
            return scope['user']
        
        fakeConnect = scope['GET'].get('fakeConnect', False)
        if fakeConnect is False:
            return scope['user']

        if scope['user'].is_anonymous is False:
            return scope['user']
        
        # -> Ce connecter avec le dernier utilisateur, inscrit dans la base de donnee
        dbUser = User.objects.all().last()
        return dbUser

        
    def load_profile(scope):
        """
            @description:
        """

        if isinstance(scope['user'], AnonymousUser):
            return None

        return Profile.objects.filter(user=scope['user'].id).first()
        # return Profile.objects.filter(user=scope['user']).first()

    def wrap(self, *args, **kwargs):
        self.scope['GET'] = websocket__readqueryparams(self.scope)
        self.scope['user'] = fakeConnect(self.scope)
        self.scope['profile'] = load_profile(self.scope)
        return function(self, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap