


class InterfaceManager(object): 
    """
        @description: This class manages the interfaces, with multiple functions. 
    """
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

    def _interface__assert__function_executed(self, function_name):
        """
            @description: Assert if the function has been executed. 
        """
        self._interface__initlog()
        for log in self._interfacelistlog:
            if log['function_name'] == function_name:
                return True
        return False
    