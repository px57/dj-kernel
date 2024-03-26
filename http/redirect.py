
from django.conf import settings
from django.shortcuts import redirect

import os

def redirectToClient(request, pathname):
    """
        @description: Rediriger cette utilisateurs vers la vu client selon les différentes conditions et position.
    """
    if settings.PRODUCTION:
        if hasattr(request, 'profile'):
            host = 'https://venture-project.com'
            return redirect(os.path.join(host, pathname))

        host = 'https://venture-project.com'
        return redirect(os.path.join(host, pathname))

    host = 'https://127.0.0.1:4200'
    return redirect(os.path.join(host, pathname))
