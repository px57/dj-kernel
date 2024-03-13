

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
        ALL_STACK.append(self)

        self.rules = {}
        self.lock_rules = {}

        # -> get the name of the stack
        # Obtenir la frame de la pile d'appels
        frame = inspect.currentframe()
        # Remonter d'un niveau pour obtenir l'endroit où la classe a été instanciée
        caller_frame = frame.f_back
        # Obtenir le nom du fichier et le numéro de ligne du caller
        filename = caller_frame.f_code.co_filename
        line_number = caller_frame.f_lineno
        # print(f"Cette classe a été instanciée dans : {filename} à la ligne {line_number}")
        self.name = filename

    def __str__(self):
        return self.name

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

        Args:
            ruleClass (class): The rule class
        """
        if ruleClass.label in self.protected_name:
            raise Exception('The name: ' + ruleClass.label + ' is protected')
        
        if self.lock_rules.get(ruleClass.label, None) is not None:
            raise Exception('The rule: ' + ruleClass.label + ' is locked')
        
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

    def __get_interface_name(self, interface_name):
        """
        Get the interface name
        1. If the interface name is a string, return the string
        2. If the interface name is a class, return the
            2.1. The label of the class
        3. If the interface name is an instance, return the
        """
        if isinstance(interface_name, str):
            return interface_name
        try:
            return interface_name().label
        except:
            return interface_name.label
        
    def get_rule(self, interface_name: str, **kwargs):
        """
        Get the rule or raise an exception.

        Args:
            interface_name (str | class): The interface name
            kwargs.raise_error_enable (bool): If the error should be raised
        """

        interface_name = self.__get_interface_name(interface_name)

        raise_error_enable = kwargs.get('raise_error_enable', True)

        if interface_name in self.rules:
            return deepcopy(self.rules[interface_name])
        
        if not raise_error_enable:
            return None
        message = """
            The interface: """ + interface_name + """ does not exist in the stack: """ + self.get_stack_path()

        raise Exception(message)
    
    def get_interface(self, interface_name: str, **kwargs):
        return self.get_rule(interface_name, **kwargs)

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
        interface_name = self.__get_interface_name(interface_name)
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
            if rule.label == DEFAULT_INTERFACE_NAME:
                continue
            choices.append((rule.label, rule.label))
        return choices
    
    def rules_choices(self, rules: str):
        """
        It returns the models choices
        """
        choices: list = []
        for _in in self.rules.values():
            _in = _in()
            if not hasattr(_in, rules):
                continue

            rules_choices_name = rules + '__rules_choices'
            if not hasattr(_in, rules_choices_name):
                raise Exception('The function: ' + rules_choices_name + ' does not exist in the class: ' + _in.label)
            rules_choices_function = getattr(_in, rules + '__rules_choices')
            choices = rules_choices_function(choices)

        return choices

    def list_rules(self):
        """
        It returns the models choices
        """
        return [rule for rule in self.rules.values()]
    
    def replace_interface(self, ruleClass):
        """
        Merge the interface

        Process:
        1. Check if the rule exists
            1.1. If the rule does not exist, set the rule in the lock_rules
        2. If the rule exists, merge the rule
        """
        self.set_rule(ruleClass)
        self.lock_rules[ruleClass.label] = ruleClass
    
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

