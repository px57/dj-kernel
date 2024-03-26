
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext as _
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User

from django import forms

import json

class InterfaceValidators(forms.Field):
    """
    Validate the interface, label.
    """
    default_validators = []

    def __init__(self, stack=None, required=True):
        """
        Initialize the validators.
        
        Args:
            stack: The stack of the validators.
            required: If the field is required.
        """
        super().__init__()
        self.stack = stack
        self.required = required

    def to_python(self, firstOrlast__name):
        return firstOrlast__name