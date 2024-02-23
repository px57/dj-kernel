"""
    Cette classe permet de charger plusieur stack en meme temps et de les configurer pour que leur design pattern 
    corresponde a ceux des differentes interfaces.

    Par exemple ont veut envoyer un emails, des notifications, des sms, des messages sur les reseaux sociaux,

    Ont creer un stackSwitcher, ont charge les stack dedier au notifications, au sms, au reseaux sociaux.

    Ensuite lorsque l'ont veut envoyer une message. 

    Ont fait:

    MESSAGE_SWITCHER.init(
        'key', 
        res, 
        {
            'message': 'Hello World'
        }
    ).send()

    Ce code va rechercher dans les stack notification, sms, etc... 

    Regarder si $INTERFACE_KEY existe, si oui, il va appeler la methode send de chaque interface.
"""

from kernel.message.error import raise_error

class InterfaceSwitcher:
    """
    Il s'agit ici des interfaces qui ont ete trouver dans les stack.
    """
    def __init__(self, interfaces):
        self.interfaces = interfaces

    def __getattr__(self, function_name):
        """
            Permet de recuperer une methode d'une interface
        """
        def wrapper(*args, **kwargs):
            for interface in self.interfaces:
                getattr(interface, function_name)(**kwargs)
        return wrapper

class StackSwitcher:
    def __init__(self):
        """
        Permet de definir un stackSwitcher

        Self 
            stack_switch: list -> Liste des stack
            process: function -> Process qui va servir a gerer les differentes interfaces.
            execute_time: string -> Permet de definir la fonction definit lors de l'appel 
                                    dynamique, s'executera au sein des interfaces, 
                                    avant ou apres.
        """
        self.stack_switch = []
        self.process = None
        self.execute_time = 'before' # or after

    def load_stack(self, stack):
        """
            Charge un stack
        """
        self.stack_switch.append(stack)

    def set_process(self, process):
        """
            Permet de definir un process qui va servir a gerer les differentes interfaces.
        """
        self.process = process
    
    def has_process(self):
        """
            Permet de verifier si un process a ete defini
        """ 
        return self.process is not None
    
    def __getattr__(self, function_name):
        """
            Permet de recuperer une methode d'une interface
        """
        def wrapper(**kwargs):
            _inSwitch = kwargs.get('_inSwitch', False)
            res = kwargs.get('res', False)
            help = kwargs.get('help', False)

            if not _inSwitch:
                raise_error('You must provide a _inSwitch object')
                
            if not res:
                raise_error('You must provide a res object')

            switcher_res = {}
            for stack in self.stack_switch:
                _in = stack.get_rule(_inSwitch)
                if not hasattr(_in, function_name):
                    raise AttributeError('The function: ' + function_name + ' does not exist in the stack: ' + _in().__class__.__name__)
                switcher_res[_in().__classpath__] = getattr(_in(), function_name)(**kwargs)

            if help:
                for resp in switcher_res:
                    print ('*** Switcher: ' + resp + ' ***')
                    print (resp)
            return switcher_res


        return wrapper
    
