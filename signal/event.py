
from typing import Callable
import pprint 

class SignalCenter(object):
    """
        @description: Signal manager class
    """

    def __init__(self):
        """
            @description: Constructor
        """
        self.signals = {}

    def create_if_not_exists(self,
        event_name: str,
        description: str=None, 
        type=None,
        data=None, 
        created_by=None, 
        created_on=None, 
        updated_by=None, 
        updated_on=None
    ):
        """
            @description: Create signal if not exists
        """
        if self.event_not_exists(event_name):
            self.create(
                event_name,
                description=description, 
                type=type,
                data=data, 
                created_by=created_by, 
                created_on=created_on, 
                updated_by=updated_by, 
                updated_on=updated_on 
            )

    def create(self, 
        event_name: str,
        description: str=None, 
        type=None,
        data=None, 
        created_by=None, 
        created_on=None, 
        updated_by=None, 
        updated_on=None
    ):
        """
            @description: Create signal
        """
        self.raise_if_event_exists(event_name)

        self.signals[event_name] = {
            'name': event_name,
            'description': description,
            'type': type,
            'data': data,
            'created_by': created_by,
            'created_on': created_on,
            'updated_by': updated_by,
            'updated_on': updated_on,
            'receptor': [],
        }

    def show_info(self, event_name: str):
        """
            @description: Show signal information
        """
        self.raise_if_event_not_exists(event_name)
        pprint.pprint(self.signals[event_name])

    def show_all_events(self):
        """
            @description: Show all events
        """
        for event_name in self.signals.keys():
            print (event_name + ' -> ' + self.formated_description(event_name))

    def formated_description(self, event_name: str):
        """
            @description: Show signal description
        """
        return ' '.join(self.signals[event_name]['description'].split())


    def event_exists(self, event_name: str):
        """
            @description: Check if event exists
        """
        return event_name in self.signals.keys()

    def event_not_exists(self, event_name: str):
        """
            @description: Check if event not exists
        """
        return not self.event_exists(event_name)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> RECEPTOR >>>>>>>>>>>>>
    def receptor_list_str(self, event_name: str) -> list:
        """
            @description: Return receptor list as string
        """
        self.raise_if_event_not_exists(event_name)
        receptor_list_str = []
        for receptor in self.signals[event_name]['receptor']:
            receptor_list_str.append(receptor.__name__)
        return receptor_list_str

    def receptor_exists(self, event_name: str, receptor: Callable):
        """
            @description: Check if receptor exists
        """
        self.raise_if_event_not_exists(event_name)
        if receptor.__name__ in self.receptor_list_str(event_name):
            return True
        return False
    
    def receptor_not_exists(self, event_name: str, receptor: Callable):
        """
            @description: Check if receptor not exists
        """
        self.raise_if_event_not_exists(event_name)
        return not self.receptor_exists(event_name, receptor)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BIND >>>>>>>>>>>>>
    def bind(self, 
        event_name: str, 
        receptor: Callable):
        """
            @description: Bind receptor to signal
        """
        self.raise_if_event_not_exists(event_name)
        self.signals[event_name]['receptor'].append(receptor)

    def unbind(self, 
        event_name: str, 
        receptor: Callable):
        """
            @description: Unbind receptor from signal
        """
        self.raise_if_event_not_exists(event_name)
        receptor_name = receptor.__name__
        i = 0
        for receptor in self.signals[event_name]['receptor']:
            if receptor == receptor_name:
                self.signals[event_name]['receptor'].pop(i)
            i += 1

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXECUTE >>>>>>>>>>>>>
    def execute(self, 
        event_name: str,
        *args,
        **kwargs
    ):
        """
            @description: Execute signal
        """
        self.raise_if_event_not_exists(event_name)
        response = {}

        for receptor in self.signals[event_name]['receptor']:
            response[receptor.__name__] = receptor(*args, **kwargs)

        return response

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXCEPTIONS >>>>>>>>>>>>>
    def raise_if_event_not_exists(self, event_name: str):
        """
            @description: Raise exception if event not exists.
        """
        if self.event_not_exists(event_name):
            raise Exception('Event not exists ' + event_name)

    def raise_if_event_exists(self, event_name: str):
        """
            @description: Raise exception if event exists.
        """
        if self.event_exists(event_name):
            raise Exception('Event exists ' + event_name)

    
SIGNAL_CENTER = SignalCenter()
