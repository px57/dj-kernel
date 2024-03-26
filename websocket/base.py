

def websocket__readqueryparams(scope):
    """
        @description:
    """
    params = {}
    if scope["query_string"]:
        for param in scope["query_string"].decode("utf-8").split("&"):
            key, value = param.split("=")
            params[key] = value
    return params

