import os

def has_modification(git_path: str):
    """
    This function is to check if the project has modification.

    Args:
    - git_path: the git path.   
    """
    pwd = os.getcwd()
    os.chdir(git_path)
    a = os.system('git status')
    os.chdir(pwd)
    return a == 0