

# load deepcopy
from copy import deepcopy

class RulesStack:
    """
        @description: Il s'agit ici d'une pile de règles, d'interface.
    """

    def __init__(self) -> None:
        """
            @description: 
        """
        self.rules = {

        } 

    def set_rule(self, ruleClass):
        """
            @description: This function sets the rule 
        """
        self.rules[ruleClass.label] = ruleClass

    def get_rule(self, interface_name: str):
        """
            @description: Get the rule or raise an exception.
        """
        if interface_name in self.rules:
            return deepcopy(self.rules[interface_name])
        
        raise Exception('The rule with the interface_name: ' + interface_name + ' does not exist')

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