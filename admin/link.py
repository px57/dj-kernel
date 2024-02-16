"""
This module contains functions to generate links to the admin page
"""

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
