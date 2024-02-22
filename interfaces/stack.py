

from django.conf import settings
from django.dispatch import receiver
from kernel.signal.boot import model_ready
from copy import deepcopy

ALL_STACK = []

class RulesStack:
    """
        @description: Il s'agit ici d'une pile de règles, d'interface.
    """

    def __init__(self) -> None:
        """
            @description: 
        """
        global ALL_STACK
        self.rules = {}
        ALL_STACK.append(self)

    def set_rule(self, ruleClass):
        """
            @description: This function sets the rule 
        """
        self.rules[ruleClass.label] = ruleClass
        self.__run_pre_init(ruleClass)

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

    def get_rule(self, interface_name: str):
        """
            @description: Get the rule or raise an exception.
        """
        if interface_name in self.rules:
            return deepcopy(self.rules[interface_name])
        
        raise Exception('The rule with the interface_name: ' + interface_name + ' does not exist')

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
        return [(rule.label, rule.label) for rule in self.rules.values()]
    
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