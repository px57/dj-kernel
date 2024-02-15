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

class StackSwitcher:
    def __init__(self):
        self.stack_switch = []

    def load_stack(self, stack):
        """
            Charge un stack
        """
        self.stack_switch.append(stack)
    
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

            for interface in callinterface:
                getattr(interface, function_name)(**kwargs)
            return self
        return wrapper
    
res = None

MESSAGE_SWITCHER = StackSwitcher()
send = MESSAGE_SWITCHER.send(
    'interfac_key',
    res,
    {
        'message': 'Hello World'
    }
)
