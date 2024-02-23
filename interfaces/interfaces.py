

from kernel.interfaces.env import DEFAULT_INTERFACE_NAME
import importlib
import os


class InterfaceManager(object): 
    """
        @description: This class manages the interfaces, with multiple functions. 
    """

    DEBUG = False

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


def __init__interface__(app: str, ) -> None:
    """
    In the app has, __interface__ folder import all modules, dynamically.   
    """
    module = app + '.__interface__'
    importlib.import_module(module)
    listdir = os.listdir(module.replace('.', '/'))
    for remove in ['__init__.py', '__pycache__']:
        if remove in listdir:
            listdir.remove(remove)
            
    for file in listdir:
        if file.endswith('.py'):
            importlib.import_module(module + '.' + file.replace('.py', ''))