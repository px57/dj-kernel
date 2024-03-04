

from kernel.interfaces.env import DEFAULT_INTERFACE_NAME
from django.conf import settings
from django.dispatch import receiver
from kernel.signal.boot import model_ready
from copy import deepcopy
import inspect


import importlib
ALL_STACK = []

class RulesStack:
    """
        @description: Il s'agit ici d'une pile de règles, d'interface.
    """

    protected_name = [
        'HELP' # Is used to display the list of interfaces rules with the help command. 
    ]

    def __init__(self) -> None:
        """
            @description: 
        """
        global ALL_STACK
        self.rules = {}
        ALL_STACK.append(self)

    def get_stack_path(self):
        """
        Get the name of the stack
        """
        # Obtenir la frame de la pile d'appels
        frame = inspect.currentframe()
        # Remonter d'un niveau pour obtenir l'endroit où la classe a été instanciée
        caller_frame = frame.f_back
        # Obtenir le nom du fichier et le numéro de ligne du caller
        filename = caller_frame.f_code.co_filename
        line_number = caller_frame.f_lineno
        print(f"Cette classe a été instanciée dans : {filename} à la ligne {line_number}")
        return filename
    
    def get_stack_name(self):
        """
        Get the name of the stack
        """
        path = self.get_stack_path()

    def set_rule(self, ruleClass):
        """
        Set the rule in the stack.
        """
        if ruleClass.label in self.protected_name:
            raise Exception('The name: ' + ruleClass.label + ' is protected')
        
        # -> TODO: check if the label is 250 characters. maximum
        try:
            ruleClass()
        except:
            raise Exception('The rule class must be callable')
        
        self.rules[ruleClass.label] = ruleClass
        self.__run_pre_init(ruleClass)

    def add_rule(self, ruleClass):
        """
        Add the rule in the stack.
        """
        return self.set_rule(ruleClass)

    def __run_pre_init(self, ruleClass):
        """
            @description: This function runs the pre init function
        """
        try: 
            ruleClass.gpm_pre_init()
        except:
            try:
                ruleClass().gpm_pre_init()
            except:
                pass

    def help(self):
        """
        Return json help
        """
        return {
            
        }

    def get_rule(self, interface_name: str, **kwargs):
        """
        Get the rule or raise an exception.

        Args:
            interface_name (str | class): The interface name
            kwargs.raise_error_enable (bool): If the error should be raised
        """
        def __get_interface_name(interface_name):
            """
            Get the interface name
            """
            if isinstance(interface_name, str):
                return interface_name
            try:
                return interface_name().label
            except:
                return interface_name.label

        interface_name = __get_interface_name(interface_name)

        raise_error_enable = kwargs.get('raise_error_enable', True)

        if interface_name in self.rules:
            return deepcopy(self.rules[interface_name])
        
        if not raise_error_enable:
            return None
        message = """
            The interface: """ + interface_name + """ does not exist in the stack: """ + self.get_stack_path()

        raise Exception(message)

    def run_rule(self, interface_name: str, *args, **kwargs):
        """
            @description: Run the rule
        """
        rule = self.get_rule(interface_name)
        if hasattr(rule, 'gpm_run'):
            return rule.run(*args, **kwargs)
        return False

    def has_rule(self, interface_name: str):
        """
            @description: Check if the rule exists
        """
        return interface_name in self.rules
    
    def not_has_rule(self, interface_name: str):
        """
            @description: Check if the rule does not exist
        """
        return not self.has_rule(interface_name)

    def models_choices(self):
        """
        It returns the models choices
        """
        choices = []
        for rule in self.rules.values():
            rule = rule()
            if rule.label is DEFAULT_INTERFACE_NAME:
                continue
            choices.append((rule.label, rule.label))
        return choices
    
    def list_rules(self):
        """
        It returns the models choices
        """
        return [rule for rule in self.rules.values()]
    
def model_ready(*args, **kwargs):
    """
    @description: This function is called when the model is ready
    """
    for stack in ALL_STACK:
        for rule in stack.list_rules():
            try:
                rule.gpm_init()
            except:
                rule().gpm_init()