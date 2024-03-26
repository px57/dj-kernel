
from django import forms

class InterfaceValidator(forms.Field):
    """
        1. Validate if BankInfoId is valide
    """
    default_validators = []

    def __init__(self, required=True):
        super().__init__()
        self.required = required

    def to_python(self, firstOrlast__name):
        return firstOrlast__name