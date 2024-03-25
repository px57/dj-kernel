
from django.core.exceptions import ValidationError
from django import forms

from gpm.models.fetch_all_models_file import existRelatedModel

class RelatedModelValidator(forms.Field):
    """
        @description:
    """
    default_validators = []

    def __init__(
            self, 
            required=True
    ):
        super().__init__()
        self.required = required

    def to_python(self, relatedModel):
        """
            @description:
        """
        if not existRelatedModel(relatedModel):
            raise forms.ValidationError('Related Model not found: ' + relatedModel)
        return relatedModel