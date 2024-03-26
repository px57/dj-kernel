"""
Is a library to simplify the path finding.
"""
import os 

def find_directory_in_parent(name, start):
    """
    Find a directory in the parent directories of the start directory
    :param name: The name of the directory to find
    :param start: The directory to start the search
    """
    current = os.path.abspath(start)
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, name)):
            return current
        current = os.path.dirname(current)
    return None