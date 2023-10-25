import os

def dockerPS_to_json():
    """
        @description: 
    """
    cmd = "docker ps --format '{{json .}}'"