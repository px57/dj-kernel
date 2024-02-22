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
        def wrapper(*args, **kwargs):
            callinterface = []
            interface_name = args[0]
            for stack in self.stack_switch:
                if stack.not_has_rule(interface_name):
                    continue
                callinterface.append(stack.get_rule(interface_name))
            
            interfaceSwitcher = InterfaceSwitcher(callinterface)

            if self.execute_time == 'before':
                interfaceSwitcher.__getattr__(function_name)(**kwargs)

            if self.has_process():
                self.process(interfaceSwitcher, function_name, **kwargs)

            if self.execute_time == 'after':
                interfaceSwitcher.__getattr__(function_name)(**kwargs)
        return wrapper
    
