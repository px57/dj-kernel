
from django.conf import settings

def django_settings_check_keys(keys):
    for key in keys:
        if not hasattr(settings, key):
            raise Exception(f"Missing required Django setting: {key}")