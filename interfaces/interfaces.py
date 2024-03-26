

from gpm.interfaces.service import Service
from gpm.interfaces.env import DEFAULT_INTERFACE_NAME

from django.conf import settings

import importlib
import os


LIST_PODDABLE_MODULE = []

class InterfaceManager(object): 
    """
        @description: This class manages the interfaces, with multiple functions. 
    """

    """
    Set the debug mode.
    """
    DEBUG = False

    """
    The response object.
    """
    res = None

    """
    The request object.
    """
    request = None

    """
    allow flag to enable or disable the rule.
    """
    allow = True

    """
    Description of the rule.
    """
    description = 'No description'

    """
    The class to call the service.
    """
    gpm_service = None

    def __init__(self, *args, **kwargs):
        """
            @description: The constructor of the interface.
        """
        self.gpm_service = Service(self)

    @property
    def __classpath__(self):
        """
            @description: The interface path.
        """
        return self.__class__.__module__ + '.' + self.__class__.__name__

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [LOG] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def _interface__initlog(self):
        """
            @description: Create the interface list log. 
        """
        if hasattr(self, '_interfacelistlog'):
            return
        self._interfacelistlog = []

    def _interface__log(self, 
        function_name='default', 
        description="", 
        args=[], 
        kwargs={}):
        """
            @description:
            @params.function_name: The name of the function
            @params.description: The description of the function
            @params.args: The arguments
            @params.kwargs: The keyword arguments 
        """
        self._interface__initlog()
        self._interfacelistlog.append({
            'function_name': function_name,
            'description': description,
            'args': args,
            'kwargs': kwargs,
        })
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [END] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [ASSERT] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def _interface__assert__function_executed(self, function_name):
        """
            @description: Assert if the function has been executed. 
        """
        self._interface__initlog()
        for log in self._interfacelistlog:
            if log['function_name'] == function_name:
                return True
        return False
    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [END] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [LABEL] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    @property
    def label(self):
        """
            @description: The label of the rule
        """
        return DEFAULT_INTERFACE_NAME

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [END] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [GPM] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def gpm_pre_init(self):
        """
            @description: The gpmInit method.
        """
        self._interface__log(function_name='gpm_pre_init')

    def gpm_init(self, *args, **kwargs):
        """
            @description: The gpmInit method.
        """
        self._interface__log(function_name='gpm_init')

    def gpm_post_init(self):
        """
            @description: The gpmInit method.
        """
        self._interface__log(function_name='gpm_post_init')

    def gpm_run(self):
        """
        The gpmRun method.
        """
        pass

    def gpm__generate__viewsactions__name(self, action='viewparams'):
        """
        Generate the views actions name.
        """
        path = self.request.path
        split = path.split('/')
        endpath = split[-2]
        endpath = endpath.replace('/', '')
        return 'gpm__' + action + '__' + endpath

    def gpm__viewparams__run(self):
        """
        Get the params and init the interface.
        """
        if self.request is None:
            raise Exception('The request object is None')
        
        path = self.request.path
        split = path.split('/')
        endpath = split[-2]
        endpath = endpath.replace('/', '')

        funtion_name = 'gpm__viewparams__' + endpath
        if not hasattr(self, funtion_name):
            raise Exception('The method ' + funtion_name + ' not found in the interface ' + self.__classpath__)

        method = getattr(self, funtion_name)
        return method()
        
def __init__interface__(app: str, ) -> None:
    """
    In the app has, __interface__ folder import all modules, dynamically.   
    """
    def __create_interface_dir(module_path):
        """
        Create the interface directory.
        """
        if not settings.DEBUG: 
            return

        if os.path.exists(module_path):
            return;

        # # Create the folder
        os.makedirs(module_path)
        # Create the __init__.py file
        with open(module_path + '/__init__.py', 'w') as f:
            f.write('')

    def __create_interface_pod(app, module, module_path):
        """
        In the interface directory create the pod file.
        """
        global LIST_PODDABLE_MODULE
        if not settings.DEBUG: 
            return
        
        for poddable_module in LIST_PODDABLE_MODULE:
            interface_pod_path = os.path.join(app, '__interface__', poddable_module + '.py')
            if os.path.exists(interface_pod_path):
                continue

            # create the file of pod.
            with open(interface_pod_path, 'w') as f:
                f.write('')
                f.write('from gpm.interfaces.interfaces import InterfaceManager\n')
                f.write('\n')
            # change the permission of the file.
            os.chmod(interface_pod_path, 0o777)

    def __import_interface_pod():
        """
        Import the interface.
        """
        importlib.import_module(module)
        listdir = os.listdir(module.replace('.', '/'))
        for remove in ['__init__.py', '__pycache__']:
            if remove in listdir:
                listdir.remove(remove)
                
        for file in listdir:
            if file.endswith('.py'):
                importlib.import_module(module + '.' + file.replace('.py', ''))

    module = app + '.__interface__'
    module_path = module.replace('.', '/')
    __create_interface_dir(module_path)
    __create_interface_pod(app, module, module_path)
    __import_interface_pod()


def message_addmethod_tointerface(_in, code_method, description_method):
    """
    Add a method to the interface.

    Args:
        _in: The interface object
        code_method: The code of the method
        description_method: The description of the method 
    """
    message = """
    Add this event method to the interface """ + _in.label + """ name of class : """ + _in.__classpath__ + """
    """ + code_method + """
    """ + description_method + """
    """
    return message

def has_stack_in_this_app(app) -> bool:
    """
    Check if the stack is in this app.
    """
    if os.path.exists(app + '/rules/stack.py'):
        return True
    return False

def init_list_poddable_module():
    """
    Init the list of poddable interfaces.
    """
    installed_apps = settings.INSTALLED_APPS
    poddable_module = []
    for app in installed_apps:
        if has_stack_in_this_app(app):
            poddable_module.append(app)

    global LIST_PODDABLE_MODULE
    LIST_PODDABLE_MODULE = poddable_module

init_list_poddable_module()