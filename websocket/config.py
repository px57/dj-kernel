from django.conf import settings

def find_consumers_files():
    """
        @description: find all consumers files, in django.APPS_INSTALLED
    """
    consumers_files = []
    for app in settings.INSTALLED_APPS:
        try:
            consumers_files.append(__import__(app + ".consumers"))
        except:
            pass
    return consumers_files

