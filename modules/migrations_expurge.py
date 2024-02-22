

# from django.conf import settings
import os


def get_migrations_path():
    """
        @description: Return the list of all migrations dir to the project.
    """
    list_migrations_path = []
    # os.walk
    for root, dirs, files in os.walk('.'):
        if 'migrations' in dirs:
            list_migrations_path.append(os.path.join(root, 'migrations'))
    
    return list_migrations_path
    # for app in settings.INSTALLED_APPS:
    #     if app != 'kernel':
    #         dirapp = app.replace('.', '/')
    #         path = os.path.join(dirapp, 'migrations')
    #         list_migrations_path.append(path)
    # return list_migrations_path

def clean_pyc():
    """
        @description: 
    """
    os.system('python3 manage.py clean_pyc')


def makemigrations():
    """
        @description:
    """
    os.system('python3 manage.py makemigrations')

def migrate():
    """
        @description:
    """
    os.system('python3 manage.py migrate')

def migration_expurge():
    """
        @description: Delete all the migrations file and run clean_pyc, and makemigrations and migrate. 
    """
    list_migrations_path = get_migrations_path()
    for migrations_path in list_migrations_path:
        if 'django' in migrations_path:
            continue
        listdir = os.listdir(migrations_path)
        for file in listdir:
            # -> Remove all 
            if os.path.isdir(os.path.join(migrations_path, file)):
                continue

            if file != '__init__.py':
                os.remove(os.path.join(migrations_path, file))

    clean_pyc()
    # makemigrations()
    # migrate()
