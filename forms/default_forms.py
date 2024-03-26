
from django import forms

class AutocompleteForm(forms.Form):
    """
    The autocomplete form.
    """
    query = forms.CharField(
        required=True,
        max_length=100,
    )

    def clean_query(self):
        """
        Clean the query.
        """
        return self.cleaned_data['query'].strip()