"""
This module contains functions to generate links to the admin page
"""

from django.utils.safestring import mark_safe

def admin_path_model_change(
        modelInterface=None,
        relatedModelId=1
    ):
    """
    Generate a link to the admin page of the related model.
    :param modelpath: the path to the model.
    :param relatedModelId: the id of the model.
    :return: the link.
    """
    module = modelInterface.__module__.replace('.models', '')
    modelpath = module + '.' + modelInterface.__name__

    modelpath = modelpath.replace('.', '/')
    modelpath = modelpath.lower()
    return u'/admin/{0}/{1}/change/'.format(
        modelpath, 
        relatedModelId
    )

def admin_model_change_html(
    modelInterface=None,
    relatedModelId=1,
    text='Change'
):
    """
    Generate a link to the admin page of the related model.
    :param modelpath: the path to the model.
    :param relatedModelId: the id of the model.
    :return: the link.
    """
    url = admin_path_model_change(
        modelInterface=modelInterface,
        relatedModelId=relatedModelId
    )
    return mark_safe('<a href="' + url + '">' + text + '</a>')