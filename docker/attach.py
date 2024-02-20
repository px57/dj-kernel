
from kernel.docker.id import get_container_id
import os

def docker_attach(container): 
    """
    Attach to a container
    """
    os.system('sudo docker attach ' + get_container_id(container))