
from django.conf import settings
import django
import pprint

def fetch_all_models_file():
    """
        @description:
            -> Cette fonction permet de récupérer tous les models de l'application
    """
    # -> On récupère tous les models de l'application
    models = settings.INSTALLED_APPS
    models_files = []
    for model in models:
        try:
            models_files.append(__import__(model + '.models', fromlist=['']))
        except Exception as e:
            pprint.pprint (e)
    return models_files


def get_models_to_file(file):
    """
        @description:
    """
    models_list = []
    for model_key in dir(file):
        # TODO: get the element with parent BaseMetadaModels
        method = getattr(file, model_key)

        if not hasattr(method, 'created_on'):
            continue
        models_list.append(method)
    return models_list

def get_list_models_to_file():
    """
        @description:
    """
    response = []
    models_files = fetch_all_models_file()
    for model_file in models_files:
        response.extend(get_models_to_file(model_file))
    return response
