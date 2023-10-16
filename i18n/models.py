# -*- coding: utf-8 -*-

from django.db.models import Q
from profiles.models import Profile


def serialize_translate(self, *args, **kwargs):
    """
        @description: Decorator to serialize translate
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def translation_model_exists(querySet):
    """
        @description:
    """
    if len(querySet) == 0:
        return False
    
    if hasattr(querySet[0], 'translation_model'):
        return True
    return False

def getNameOfModelWithQuerySet(querySet):
    """
        @description:
    """
    for result in querySet:
        if not hasattr(result, '__class__'):
            continue
        if not hasattr(result.__class__, '__name__'):
            continue

        return result.__class__.__name__

    return 'aeuoae'
    

def translateDBQuerySet(**kwargs):
    """
        @description: 
        @usage:
            translateDBQuerySet(
                model_to_serialize=Guides,
                querySet=Guides.objects.filter(activated=True),
            )
    """
    def required(data, message):
        """
            @description:
        """ 
        if data is None:
            raise Exception(message)
        
    default_params = {
        'autoload_profile': True,
    }
    kwargs = {**default_params, **kwargs}
        
    request = kwargs.get('request')
    querySet = kwargs.get('querySet')

    required(request, 'Request is required to translateDBQuerySet')
    required(querySet, 'QuerySet is required to translateDBQuerySet')

    if not hasattr(request, 'profile') and kwargs.get('autoload_profile'):
        request.profile = Profile.objects.get(user=request.user)
    
    if request.profile.language == 'en':
        return querySet

    query = Q()
    for result in querySet:
        query |= Q(translateObject=result)
 
    if len(querySet) == 0:
        return querySet
    
    if not translation_model_exists(querySet):
        raise Exception('Translation model does not defined to model class ' + getNameOfModelWithQuerySet(querySet))

    translation_model = querySet[0].translation_model
    dbTranslate = translation_model.objects.filter(query)

    # -> merge the translate with the querySet
    for translate in dbTranslate:
        for result in querySet:
            if result.id == translate.translateObject.id:
                result._TRANSLATE = translate

    return querySet


def translateDBObject(request, object):
    """
        @description: 
    """
    if object is None:
        return None
    return translateDBQuerySet(
        request=request,
        querySet=[object],
    )[0]