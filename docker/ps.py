
import os

def dockerPS_to_json():
    """
        @description: 
    """
    cmd = "docker ps --format '{{json .}}'"
    return os.popen(cmd).read()

def choice_docker_container():
    """
        @description: 
    """
    cmd = "docker ps --format '{{.Names}}'"
    return os.popen(cmd).read()
