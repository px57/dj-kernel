# -*- coding: utf-8 -*-
"""Docstrings."""

from django.test import TestCase
from kernel.http.request import generate_fake_request
from sites.models import Site
from kernel.http.classobjects import Url

import pprint
import os

try:
    from django.http import JsonResponse
    from django.conf import settings
except Exception:
    pass

import json


class ResponseCore:
    """Contains params used in response."""
    error_code = {
        '404': "Not Found !!"
    }

    def __init__(self, child_class):
        """
            @description: 
        """
        self.child_class = child_class
        self.first_run = True
        self.content = {
            'success': False,
        }
        self.request = None

    def initEnd(self):
        """
            @description: The initialisation in ended. 
        """
        self.first_run = False

    def set_conf(self, kwargs):
        """
            @description: Recept configuration to Response class.
        """
        kwargs.setdefault('response_raw', False)
        for key in ['response_raw']:
            setattr(self, key, kwargs[key])

    def _return_response(self):
        if self.response_raw:
            return self.content

        if settings.DEBUG:
            pprint.pprint ("return formated http response")

        return JsonResponse(self.content, json_dumps_params={'indent': 2})

    def _clean_error(self, error_update):
        """
            @description: Clean error response. 
        """
        res = {}
        for key in error_update:
            if error_update.get(key) is None:
                continue
            res[key] = error_update.get(key)
        return res


class Response(object):
    """
        @description: Class adapted for response in views function. 
    """ 

    __core__ = {}

    def __init__(self, **kwargs):
        """Define the response settings."""
        """
        --> IJ remove a letter u defore
            kwargs.response_raw <boolean>
            ---- Retourne un self.content sous forme d'object python si True
        """
        request = None
        if kwargs.get('request'):
            request = kwargs.get('request')
            del kwargs['request']

        self.__core__ = ResponseCore(self)
        self.__core__.set_conf(kwargs)
        self.__core__.initEnd()
        self.set_request(request)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [REQUEST] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def set_request(self, request):
        """
            @description: Set request in response.
        """
        self.__core__.request = request

    def get_request(self, fake=False):
        """
            @description: Get request in response.
        """
        self.raise_error_if_no_request()
        return self.__core__.request
    
    def raise_error_if_no_request(self):    
        """
            @description: Raise error if no request.
        """
        if not self.has_request():
            raise Exception("The request is not defined in the response.")
        
    def has_request(self):
        """
            @description: Has request in response.
        """
        return self.__core__.request is not None

    def is_authenticated(self):
        """
        The user is authenticated.
        """
        return self.get_request().user.is_authenticated
    
    def is_not_authenticated(self):
        """
        The user is not authenticated.
        """
        return not self.is_authenticated()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [END] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [INTERFACE] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def get_interface(self):
        """
            @description: Get interface in request.
        """
        return self.__core__.request.interface
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [END] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [SITE] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def get_site(self):
        """
            @description: Get site in request.
        """
        if self.has_request():
            request = self.get_request()
            # get host from request
            host = request.get_host()
            return 
        
    def get_host(self) -> str:
        """
            @description: Get site in request.s
        """
        host = 'localhost:4200'
        if self.has_request():
            request = self.get_request()
            host = request.get_host()
        return host

    def get_request_protocol(self) -> str:
        """
            @description: Get site in request.
        """
        protocol = 'http'
        if self.has_request():
            request = self.get_request()
            protocol = request.scheme
        return protocol

    def create_client_url(
        self, 
        pathname: str,
        queryParams: dict = None,
        ) -> str:
        """
            @description: Get site in request.
            @param.pathname: The pathname of the url.   
            @param.queryParams: The query params of the url.
        """
        url = Url(
            protocol=self.get_request_protocol(),
            host=self.get_host(),
            pathname=pathname,
            queryParams=queryParams,
        )
        return url.compose_url()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [END] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def restResponse(self, globals, request, function):
        """
            @description: Il s'agit d'une interface REST adapter a ma logique de programmation.
            @params.request: Il s'agit tout betement de la requete http que l'ont n'a obtenu en parametre dans notre vu.
            @params.function: Le nom de la fonction a appeler.
        """
        key = function + '_' + request.method
        return globals[key](request, self)

    def success(self, **kwargs):
        """Return success JsonResponse."""
        self.__core__.content['success'] = True
        return self.__core__._return_response()

    def error(self, error=None, code_error=None, error_descr=None):
        """
            *** Return JsonResponse with error. ***
            self.error("The error message")
            self.error(403, "the messages of error")
        """
        self.__core__.content['success'] = False
        update = {}

        if type(error) == str:
            update = {
                'code_error': code_error,
                'error': error,
                'error_descr': error_descr,
            }
        elif self.__core__.error_code.get(str(error)):
            str_error = str(error)
            update = {
                'code_error': error,
                'error': self.__core__.error_code.get(str_error),
                'error_descr': code_error,
            }
        update = self.__core__._clean_error(update)
        self.update(update)
        return self.__core__._return_response()

    def warning_snackbar(self, messages=""):
        self.snackbar = {'type': 'warning', 'messages': messages}
        return self.error()

    def error_snackbar(self, messages=""):
        self.snackbar = {'type': 'error', 'messages': messages}
        return self.error()

    def default_snackbar(self, messages=""):
        self.snackbar = {'type': 'default', 'messages': messages}
        return self.success()

    def success_snackbar(self, messages=""):
        self.snackbar = {'type': 'success', 'messages': messages}
        return self.success()

    def return_content(self):
        """Return the content by taking in consideration the type of success."""
        if self.__core__.content.get('success'):
            return self.success()
        else:
            return self.error()

    def getAll(self, *args, **kwargs):
        """Get all content in self.content."""
        return self.__core__.content

    def form_error(self, form):
        """Set form result in self.__core__.content."""
        err = {}
        for item in form.errors.items():
            item[1]
            if item[1][0] == 'This field is required.':
                err[item[0]] = ['required']    
                continue
            err[item[0]] = item[1]
            
        self.form_error = err
        return self.error(404, "Invalid form post.")

    def set(self, key, value):
        """Set value in self.__core__.content."""
        self.__core__.content[key] = value

    def serialize_querySet(self, querySet, set_values='*', excludeValues=None):
        """Set query set in response."""


    def update(self, *args):
        """
            @description: Dict.update fonction.
        """
        self.__core__.content.update(*args)

    def __isCoreElem__(self, key):
        """__isCoreElem__."""
        return bool('__' in [key[0:2], key[-2:]])

    def __editattr__error(self, key):
        """Run error when the attr is modified."""
        is_core_elem = self.__isCoreElem__(key)

        if key == '__core__':
            return True

        if self.__core__.first_run and is_core_elem:
            return True

        if is_core_elem:
            err = "Not has possibility insert __func__ in Response class"
            raise Exception(err)

        return False

    def __setattr__(self, key, value):
        """__setattr__"""
        if self.__editattr__error(key):
            return super(Response, self).__setattr__(key, value)

        self.__core__.content[key] = value

    def __delattr__(self, key):
        """__delattr__."""
        if self.__editattr__error(key):
            return super(Response, self).__delattr__(key)

        del self.__core__.content[key]

    def __getattr__(self, key):
        """__getattr__."""
        if self.__isCoreElem__(key):
            return getattr(super(Response, self), key)
        return self.__core__.content[key]

    # --------------- [ITEM]
    # def __setitem__(self, key, value):
    #     """__setitem__."""
    #
    # def __delitem__(self, key):
    #     """__delitem__."""
    #
    # def __getitem__(self, key):
    #     """__getitem__."""

    def __str__(self):
        """__str__."""
        return json.dumps(self.__core__.content)


class responseSet__QuerySet(object):
    """
        @description:
    """
    def __init__(self, 
        querySet, 
        setValues='*', 
        excludeValues=None):
        """
            @description: Docstrings.
        """
        self.querySet = querySet
        self.define_set_values(setValues)
        self.define_exclude(excludeValues)

    def define_set_values(self, setValues='*'):
        """
            @description: Define setValues.
        """
        if setValues == '*':
            # Recuperer la liste des elements a recuperer
            pass
        elif type(setValues) == str:
            setValues = [setValues]
        elif type(setValues) != list:
            err_msg = 'setValue cannot be of the type "{}".'.format(type(setValues))
            raise TypeError(err_msg)
        self.setValue = setValues

    def define_exclude(self, excludeValues=None):
        """
            @description:
        """
        if excludeValues is None:
            excludeValues = []
        elif type(excludeValues) != list:
            excludeValues = [excludeValues]
        elif type(excludeValues) != list:
            err_msg = 'excludeValues cannot be of the type "{}".'.format(type(setValues))
            raise TypeError(err_msg)
        self.excludeValues = excludeValues


class ResponseTest(TestCase):
    """
        @description: Class adapted for response in views function.
    """

    def _convertValueToDict(self, value):
        """
            @description: Convert value to dict.
        """
        if type(value) == dict:
            return value
        elif type(value) == str:
            return json.loads(value)
        elif type(value) == bytes:
            return json.loads(value.decode('utf-8'))
        return {}

    def assertSuccess(self, value):
        """
            @description: Set value, string or dict, observe if the value is success -> true.
            @return: Return formated value.
        """
        value = self._convertValueToDict(value)
        self.assertTrue(value.get('success'))
        return value

    def assertError(self, value): 
        """
            @description: Set value, string or dict, observe if the value is success -> false.
            @return: Return formated value.
        """
        value = self._convertValueToDict(value)
        self.assertFalse(value.get('success'))
        return value
    
def get_fake_response(profile=None):
    """
        @description: Return a fake response.
    """
    fake_request = generate_fake_request(profile=profile)
    return Response(request=fake_request)

def load_response(function, *args, **kwargs):
    """
    Charge le profile à l'intérieurs des éléments.
    """
    def wrap(request, *args, **kwargs):
        res = Response(request=request)
        # TODO: Ajouter un systeme pour pouvoir charger l'interface, qui va servir a parametre l'execution de la view.
        return function(res, request, *args, **kwargs)
    
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
