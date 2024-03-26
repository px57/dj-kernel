
from django.conf import settings

import importlib

class Service:
    """
    Interface for binding service to a specific interface.
    """

    def __init__(self, _in) -> None:
        """
        Initialize the service.

        Args:
            _in (str): The interface to bind to.
        """
        self.service = None
        self._in = _in
        self.res = _in.res
        self.request = _in.request

    def load_service(self):
        """
        Load the service.
        """
        if not hasattr(self._in, 'service_module'):
            raise AttributeError('The interface must have a service_module attribute')
        if not hasattr(self._in, 'service'):
            raise AttributeError('The interface must have a service attribute')
        
        service = importlib.import_module(self._in.service_module + '.' + self._in.service + '.service')
        
        if not hasattr(service, 'Service'):
            raise AttributeError('The service must have a Service class')

        runned_service = service.Service()
        return runned_service

    def __getattr__(self, name):
        """
        Get the attribute of the service.

        Args:
            name (str): The name of the attribute.
        """
        if self.service is None:
            self.service = self.load_service()

        if hasattr(self.service, name):
            return getattr(self.service, name)
        else:
            raise AttributeError('The service ' + self._in.service + ' does not have the attribute ' + name)
        
class ServiceManager:
    """
    The service manager class.
    """

    def __init__(self) -> None:
        """
        The constructor method.
        """
        self.config = None
        self._in = None
        print ('ServiceManager')

    def set_config(self, _in):
        """
        Load the configuration of the service.

        Args:
            _in (str): The interface to bind to.
        """
        self.res = _in.res
        self._in = _in
        self.request = _in.request
        

        if not hasattr(_in, 'settings_config_name'):
            raise AttributeError('The interface must have a service_config_name attribute')
        
        if not hasattr(settings, _in.settings_config_name):
            raise AttributeError('The settings does not have the attribute ' + _in.settings_config_name)
        
        if not hasattr(_in, 'service_config_name'):
            raise AttributeError('The interface must have a service_config_name attribute')
        
        config_list = getattr(settings, _in.settings_config_name)
        if _in.service_config_name not in config_list:
            raise AttributeError('The settings does not have the attribute ' + _in.settings_config_name + ' with the attribute service_config_name')
        
        self.config = config_list[_in.service_config_name]

        return self.config
    
    def get_config(self):
        """
        Get the configuration of the service.
        """
        return self.config