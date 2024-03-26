from django.forms.models import model_to_dict
import pprint

def serializer__init__(fonction):
    def main(self, *args, **kwargs):
        result = fonction(self, *args, **kwargs)
        self._LOAD = {}
        self._TRANSLATE = None
        return result
    
    return main

def serializer__serialize__(fonction):
    def serialize_list(self, value):
        """
            @description:
        """
        new_list = []
        for item in value:
            new_list.append(serialize_switch(self, item)) 
        return new_list

    def serialize_dict(self, values):
        """
            @description: 
        """
        new_dict = {}   
        for key, value in values.items():
            new_dict[key] = serialize_switch(self, value)
        return new_dict
            
    def serialize_switch(self, value):
        """
            @description:
        """
        if type(value) == dict:
            return serialize_dict(self, value)
        elif type(value) == list:
            return serialize_list(self, value)
        elif type(value) == str:
            return value
        elif type(value) == int:
            return value
        
        # -> is django queryset 
        if hasattr(value, 'serialize'):
            return value.serialize(self.request)
        
        return value

    def main(self, request, *args, **kwargs):
        """
            @description: 
        """
        self.request = request
        serialized = fonction(self, request, *args, **kwargs)

        # -> LOAD
        if hasattr(self, '_LOAD'):
            serialize_load = serialize_dict(self, self._LOAD)
            serialized.update(serialize_load)
        
        # -> TRANSLATE 
        if hasattr(self, '_TRANSLATE') and self._TRANSLATE is not None:
            if hasattr(self._TRANSLATE, 'serialize'):
                try: 
                    new_data_serialized = self._TRANSLATE.serialize(request)

                    if 'id' in new_data_serialized:
                        del new_data_serialized['id']

                    if 'translateObject' in new_data_serialized:
                        del new_data_serialized['translateObject']

                    serialized.update(new_data_serialized)
                except Exception as e:
                    pass
            else: 
                new = model_to_dict(self._TRANSLATE)
                serialized.update(new)

        return serialized
    
    return main