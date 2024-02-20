

from django.db import models
from kernel.models.serialize import serializer__serialize__, serializer__init__


class BaseMetadataModel(models.Model):
    """
        @description:
    """

    @serializer__init__
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    activated = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        'created at',
        null=True,
        help_text="The object's creation date/time",
        auto_now=False,
        auto_now_add=True,
    )
    
    created_on = models.DateTimeField(
        'created on',
        null=True,
        help_text="The object's creation date/time",
        auto_now=False,
        auto_now_add=True,
    )
    updated_on = models.DateTimeField(
        'updated on',
        null=True,
        editable=False,
        help_text="The object's last update date/time",
        auto_now=False,
        auto_now_add=True,
    )

    def set_to_load(self, key, value): 
        """
            @description: 
        """
        self._LOAD[key] = value

    def run_save(self, save):
        """
            @description: 
        """
        if save:
            self.save()


    class Meta:
        abstract = True
        get_latest_by = 'updated_on'
        ordering = ['-updated_on']