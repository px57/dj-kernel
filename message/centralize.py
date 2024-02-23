
from kernel.message.error import raise_error
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

def switcher_send_message(
        _inSwitch=False, 
        res=False,
        sendTo=False,
        sendBy=False, 
        params=False
    ):
    """
    Send message to the message switcher.

    Args:
        _inSwitch: The switcher object.
        res: The response object.
        sendTo: Send to profile or Array<profile> 
        sendBy: Send by profile or Array<profile>
        params: The params object.
    """
    if not sendTo:
        raise_error('You must provide a sendTo object')

    if not sendBy:
        raise_error('You must provide a sendBy object')
    
    if not params:
        raise_error('You must provide a params object')

    return MESSAGE_SWITCHER.send(
        _inSwitch=_inSwitch,
        res=res,
        sendTo=sendTo,
        sendBy=sendBy,
        params=params,
    )