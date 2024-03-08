
from kernel.http import Response
import json


from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from kernel.http.response import Response

def add_profile(request):
    return request

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def get_interface_name_in_request(request):
    """
    Get the interface in request.
    """
    if '_in' in request.GET:
        return request.GET.get('_in').upper()
    return None
            
    interface: str | None = __get_interface_name_in_request(request)
    if type(interface) == str:
        interface = interface.upper()
    return interface

def load_help(res=None):
    """
    Charge le profile à l'intérieurs des éléments.
    """
    stack = res.get_stack()
    list_rules = stack.list_rules()
    res.title = "Help"
    res.interface_list = {}
    for rule in list_rules:
        if not hasattr(rule, 'description'):
            res.interface_list[rule.label] = 'No description'
            continue
        res.interface_list[rule.label] = rule.description

def load_response__json(request, res, _json) -> bool:
    """
    Load the response in json mode.
    """
    if not _json:
        return False
    
    try:
        request.POST = json.loads(request.body.decode('utf-8'))
    except:
        pass
    return True

def load_response__form(_in, request, res, form) -> bool:
    """
    Valid the form, in the interface and return the result.
    """
    if not form:
        return True

    params = {
        '_in': _in,
    }
    params.update(request.POST)
    _in.form = form(params)
    request.form = _in.form
    if not _in.form.is_valid():
        return False
    return True

def load_response__load_params(_in, gpm__viewparams__run):
    """
    Run the interface loader before run the view.
    """
    if not gpm__viewparams__run:
        return
    
    if type(_in.request.POST) != dict:
        _in.request.POST = _in.request.POST.dict()
    _in.request.POST.update(_in.gpm__viewparams__run())
    print (_in.request.POST)

def load_response(
        stack=None,
        debug=False,
        load_params=False,
        form=None,
        json=False,
        permission=None,
    ):
    """
    Load the response, into view.
    
    Args:
        stack: The stack of the application.
        debug: The debug mode.
        load_params: Run the interface loader before run the view.
        form: The form of the interface.
        json: The json mode.
        permission: The permission of the user.
    """
    def decorator_load_response(function, *args, **kwargs):
        """
        Charge le profile à l'intérieurs des éléments.
        """
        def wrap(request, *args, **kwargs):
            res = Response(request=request)
            res.set_stack(stack)
            kwargs['res'] = res
            _in_label = get_interface_name_in_request(request)

            if _in_label == 'HELP':
                load_help(res)
                return res.error('HELP')

            if stack.has_rule(_in_label):
                _in = stack.get_rule(_in_label)()
                _in.request = request
                _in.res = res
                _in.DEBUG = debug
                res.set_interface(_in)

                load_response__json(request, res, json)
                load_response__load_params(_in, load_params)
                if not load_response__form(_in, request, res, form):
                    return res.form_error(_in.form)
            else: 
                return res.error('The interface does not exist.')
            
            return function(request, *args, **kwargs)
        
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return decorator_load_response

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