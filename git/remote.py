"""
This module is used to manage remote git repositories.
"""

import os
import subprocess
import sys
from kernel.path.find import find_directory_in_parent

def get_remote_url():
    """
    This function is to get the remote url of the git repository
    """
    root_path = find_directory_in_parent(".git", '.')
    if not root_path:
        print ("The current directory is not a git repository")
        sys.exit(1)
    
    remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], cwd=root_path)
    remote_url = remote_url.decode("utf-8").strip()
    return remote_url

def get_repository_name():
    """
    This function is to get the repository name
    """
    remote_url = get_remote_url()
    repository_name = os.path.basename(remote_url)
    repository_name = repository_name.replace(".git", "")
    return repository_name