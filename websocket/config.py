from django.conf import settings

def find_consumers_files():
    """
        @description: find all consumers files, in django.APPS_INSTALLED
    """
    consumers_files = []
    for app in settings.INSTALLED_APPS:
        module = __import__(app)
        if hasattr(module, "consumers"):
            consumers_files.append(module)
    print (consumers_files)
    return consumers_files



