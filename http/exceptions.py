

class ExitResponse(Exception):
    """
    Exception raised when access to a certain interface is denied.
    """
    def __init__(self,
        res=None
    ):
        
        self.res = res
        super().__init__('')