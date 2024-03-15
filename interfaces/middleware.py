# interface_manager/middleware.py

from django.http import HttpResponseBadRequest

from kernel.http.exceptions import ExitResponse
from kernel.http import Response
import kernel

class InterfaceManagerMiddleware:
    """
    Middleware to manage interfaces based on user permissions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request.
        """
        return self.get_response(request)