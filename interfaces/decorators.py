

from kernel.interfaces.env import DEFAULT_INTERFACE_NAME
import functools

def load_interface(interface_stack=None, factor=1):
    # assert callable(f_py) or f_py is None
    def _decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            
            if not hasattr(request, 'POST'):
                interface = interface_stack.get_rule(DEFAULT_INTERFACE_NAME)
                request.interface = interface
                return func(*args, **kwargs)

            interface_name = args[0].POST.get('interface_name')
            if interface_name is None:
                interface_name = args[0].GET.get('interface_name')

            interface_name = DEFAULT_INTERFACE_NAME           
            interface = interface_stack.get_rule(interface_name)
            request.interface = interface
            return func(*args, **kwargs)
        return wrapper
    return _decorator(interface_stack) if callable(interface_stack) else _decorator
