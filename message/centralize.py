
from kernel.interfaces.switcher import StackSwitcher

def process(*args, **kwargs):
    """
    Run the process of message. 
    """
    print ('##' * 123)
    print (args)
    print (kwargs)

MESSAGE_SWITCHER = StackSwitcher()
MESSAGE_SWITCHER.set_process(process)

def switcher_send_message(*args, **kwargs):
    """
    Send message to the message switcher.
    """
    MESSAGE_SWITCHER.process(*args, **kwargs)

