from kernel.strapi.client import strapi_userId

def load_user_id(function):
    """
        @description: Charger la bonne langue au bon moment.
    """
    def wrap(request, *args, **kwargs):
        """
            @description: Est destiner à la récupérations automatique des informations concernants le group zone demander.
        """
        request.user_id = strapi_userId(request)
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
