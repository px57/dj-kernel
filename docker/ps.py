
import os
import docker
import json

def dockerPS_to_json():
    """
        @description: 
    """
    # Connexion au client Docker
    client = docker.from_env()

    # Récupération des conteneurs en cours d'exécution
    containers = client.containers.list()

    # Conversion des conteneurs en format JSON
    json_data = []
    for container in containers:
        json_data.append(container.attrs)

    # Affichage du résultat
    # print(json.dumps(json_data, indent=2))

def choice_docker_container():
    """
        @description: 
    """
    # cmd = "docker ps --format '{{.Names}}'"
    # return os.popen(cmd).read()
    dockerPS_to_json()
