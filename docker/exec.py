

from kernel.docker.id import get_container_id
import os 

def docker_exec_bash(container):
    os.system(f"docker exec -it {get_container_id(container)} bash")