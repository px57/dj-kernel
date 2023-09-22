from django.forms import model_to_dict


def serializer_object(function):
    """Charge le profile a l'interieurs des elements. 
    re

    Args:
        request.page_profile): Ajoute le profile chargee just ici
    """
    def serializer_object_required(serialized):
        """
            @description: 
        """
        # -> _exclude field is required
        required_list = ['_exclude', '_include', '_object']
        for required in required_list:
            if required not in serialized:
                raise Exception('The field "' + required + '" is required into the serialized object')
            
    def serializer_exclude(object, exclude):
        """
            @description: 
        """
        for field in exclude:
            if field in object:
                del object[field]
        return object
        
    def wrap(self, *args, **kwargs):
        serialized = function(self, *args, **kwargs)
        serializer_object_required(serialized)

        _object = model_to_dict(serialized['_object'])
        if '_update' in serialized:
            _object.update(serialized['_update'])
        
        return serializer_exclude(_object, serialized['_exclude'])

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap